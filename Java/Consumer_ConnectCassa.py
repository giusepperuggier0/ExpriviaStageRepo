from confluent_kafka import Consumer, KafkaException, KafkaError
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
}
TOPIC = "test"

CASSANDRA_HOSTS = ["127.0.0.1"]
KEYSPACE = "my_space"

def connect_cassandra():
    try:
        cluster = Cluster(CASSANDRA_HOSTS)
        session = cluster.connect()
        session.set_keyspace(KEYSPACE)
        
        
        session.execute("""
        CREATE TABLE IF NOT EXISTS prima_tabella (
            id UUID PRIMARY KEY,
            colonna1 TEXT,
            colonna2 TEXT,
            colonna3 TEXT,
            colonna4 TEXT
        )
        """)
        
        return cluster, session
    except Exception as e:
        print(f"Errore di connessione a Cassandra: {e}")
        raise

def consume_messages():
    """Consuma messaggi da Kafka e li inserisce in Cassandra."""
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])
    
    try:
        cluster, session = connect_cassandra()
        
        # Preparazione della query di inserimento
        insert_query = SimpleStatement("""
            INSERT INTO prima_tabella (id, colonna1, colonna2, colonna3, colonna4)
            VALUES (uuid(), %s, %s, %s, %s)
            """)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"EOF topic {msg.topic()} [{msg.partition()}] offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                
                message = msg.value().decode("utf-8") # Decodifica il messaggio CSV
                
                
                row_data = message.split(',') # Supponiamo che i dati siano separati da virgole
                # Assumiamo che il formato sia: colonna1, colonna2, colonna3, colonna4
                if len(row_data) == 4:
                    colonna1 = row_data[0]
                    colonna2 = row_data[1]
                    colonna3 = row_data[2]
                    colonna4 = row_data[3]
                

                    session.execute(insert_query, (colonna1, colonna2, colonna3, colonna4))
                    print(f"Dati inseriti in Cassandra: {colonna1}, {colonna2}, {colonna3}, {colonna4}")
                else:
                    print("Formato del messaggio errato")
                            
    except KeyboardInterrupt:
        print("\nInterruzione del consumer.")
    except Exception as e:
        print(f"Errore durante il consumo dei messaggi: {e}")
    finally:
        consumer.close()
        if 'cluster' in locals():
            cluster.shutdown()


if __name__ ==  "__main__":
    consume_messages()
