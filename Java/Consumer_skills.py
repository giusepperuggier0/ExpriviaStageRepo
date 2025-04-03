from confluent_kafka import Consumer
from cassandra.cluster import Cluster
import json
import uuid

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'cv-consumer-group',
    'auto.offset.reset': 'earliest'
}

TOPIC = "skills"

CASSANDRA_HOSTS = ["127.0.0.1"]
KEYSPACE = "cv_skills"
TABLE_NAME = "candidates_skills"

def connect_cassandra():
    try:
        cluster = Cluster(CASSANDRA_HOSTS)
        session = cluster.connect()
        
        session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        
        session.execute(f"""
        CREATE TABLE IF NOT EXISTS {KEYSPACE}.{TABLE_NAME} (
            id UUID PRIMARY KEY,
            name TEXT,
            surname TEXT,
            email TEXT,
            phone TEXT,
            date_of_birth TEXT,
            recent_work_experience TEXT,
            work_skills LIST<TEXT>,
            language_skills LIST<TEXT>
        )
        """)
        
        session.set_keyspace(KEYSPACE)
        return cluster, session
    except Exception as e:
        print(f"Errore connessione Cassandra: {e}")
        raise

def insert_data(session, cv_data):
    try:
        query = f"""
        INSERT INTO {TABLE_NAME} (
            id, name, surname, email, phone, date_of_birth,
            recent_work_experience, work_skills, language_skills
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Se work_skills o language_skills sono None, sostituisci con lista vuota
        work_skills = cv_data.get("work_skills", []) or []
        language_skills = cv_data.get("language_skills", []) or []
        
        session.execute(query, (
            uuid.uuid4(),
            cv_data.get("name", ""),
            cv_data.get("surname", ""),
            cv_data.get("email", ""),
            cv_data.get("phone", ""),
            cv_data.get("date_of_birth", ""),
            cv_data.get("recent_work_experience", ""),
            work_skills,
            language_skills
        ))
        print(f"Dati inseriti per {cv_data.get('name')} {cv_data.get('surname')}")
    except Exception as e:
        print(f"Errore inserimento dati per {cv_data.get('name', 'unknown')}: {e}")

def process_message(msg_value):
    try:
        data = json.loads(msg_value.decode('utf-8'))
        
        # Se è una lista, processa ogni elemento
        if isinstance(data, list):
            return data
        # Se è un dizionario singolo, mettilo in una lista
        elif isinstance(data, dict):
            return [data]
        else:
            print(f"Formato messaggio non supportato: {type(data)}")
            return []
    except Exception as e:
        print(f"Errore decodifica messaggio: {e}")
        return []

def consume_messages():
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])
    
    try:
        cluster, session = connect_cassandra()
        
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Errore Kafka: {msg.error()}")
                continue
                
            candidates_data = process_message(msg.value())
            for cv_data in candidates_data:
                try:
                    insert_data(session, cv_data)
                except Exception as e:
                    print(f"Errore elaborazione candidato: {e}")
                
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta...")
    except Exception as e:
        print(f"Errore generale: {e}")
    finally:
        consumer.close()
        if 'cluster' in locals():
            cluster.shutdown()

if __name__ == "__main__":
    consume_messages()