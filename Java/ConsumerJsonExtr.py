from confluent_kafka import Consumer
from cassandra.cluster import Cluster
import json
import uuid
from datetime import datetime

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
}

TOPIC = "test1"

CASSANDRA_HOSTS = ["127.0.0.1"]
KEYSPACE = "my_space"
TABLE_NAME = "json_data"

def connect_cassandra():
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)
    return cluster, session

def insert_data(session, json_data):  
    query = f"""
    INSERT INTO {TABLE_NAME} (id, name, surname, address, email, phone, work_experience, date_of_birth)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        uuid.uuid4(),
        json_data.get("name", "").strip(),
        json_data.get("surname", "").strip(),
        json_data.get("address", "").strip(),
        json_data.get("email", []) if isinstance(json_data.get("email"), list) else None,
        json_data.get("phone", []) if isinstance(json_data.get("phone"), list) else None,
        json_data.get("work_experience", []) if isinstance(json_data.get("work_experience"), list) else None,
        json_data.get("date_of_birth", "").strip(),
    )
    
    session.execute(query, values)
    print("Dati inseriti con successo!")

def consume_messages():
    
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])
    
    cluster, session = connect_cassandra()
    
    try:
        while True:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            try:
                json_data = json.loads(msg.value().decode('utf-8'))
                insert_data(session, json_data)
                
            except json.JSONDecodeError:
                print("Errore: il messaggio non è un JSON valido")
            except Exception as e:
                print(f"Errore nell'elaborazione: {e}")
                
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta, chiusura...")
    finally:
        consumer.close()
        cluster.shutdown()

if __name__ == "__main__":
    consume_messages()
