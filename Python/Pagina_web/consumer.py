from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import os

# Configurazione Kafka
KAFKA_BROKER = 'localhost:9092'  # Modifica con il tuo broker
KAFKA_TOPIC = 'invoice'  # Nome del topic Kafka

# Configurazione Cassandra
CASSANDRA_HOST = 'localhost'  # Modifica con il tuo host Cassandra
CASSANDRA_PORT = 9042
KEYSPACE = 'my_space'  # Modifica con il tuo keyspace

# Funzione per connettersi a Cassandra
def get_cassandra_connection():
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(KEYSPACE)
    return session

# Funzione per creare una tabella dinamica per ogni file
def create_table(session, file_name):
    # Modifica il nome della tabella per evitare caratteri speciali
    table_name = file_name.replace('.csv', '').replace('-', '_').replace('[', '').replace(']', '').lower()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        data TEXT,
        ora TEXT,
        livello_idrometrico FLOAT,
        temperatura_acqua FLOAT,
        temperatura_aria FLOAT,
        umidita_relativa FLOAT,
        pressione_atmosferica FLOAT,
        direzione_vento FLOAT,
        velocita_vento FLOAT,
        PRIMARY KEY (data, ora)
    );
    """
    try:
        session.execute(create_table_query)
        print(f"Tabella {table_name} creata o già esistente.")
    except Exception as e:
        print(f"Errore nella creazione della tabella {table_name}: {e}")

# Funzione per inserire i dati nella tabella specifica
def insert_data(session, file_name, row_data):
    table_name = file_name.replace('.csv', '').replace('-', '_').replace('[', '').replace(']', '').lower()
    insert_query = f"""
    INSERT INTO {table_name} (data, ora, livello_idrometrico, temperatura_acqua, temperatura_aria,
    umidita_relativa, pressione_atmosferica, direzione_vento, velocita_vento) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        session.execute(insert_query, row_data)
        print(f"Dati inseriti nella tabella {table_name}: {row_data}")
    except Exception as e:
        print(f"Errore nell'inserimento dei dati nella tabella {table_name}: {e}")

def validate_and_clean_data(row_data):
    # Controlliamo se la riga ha 10 colonne (includendo il nome del file)
    if len(row_data) >= 9:
        # Ignoriamo la prima colonna (nome del file) e prendiamo le successive 9 colonne
        row_data = row_data[1:]
    
    # Controlliamo se la riga ha esattamente 9 colonne
    if len(row_data) != 9:
        print(f"Riga non valida (numero di colonne errato): {row_data}")
        return None

    cleaned_data = []
    for value in row_data:
        # Se il valore è una stringa vuota, lo impostiamo come None
        if value == "":
            cleaned_data.append(None)
        else:
            # Se il valore è numerico (con virgola o punto), convertilo in float
            if value.replace(",", "").replace(".", "").lstrip('-').isdigit():
                cleaned_data.append(float(value.replace(",", ".")))
            else:
                # Se non è numerico, mantienilo come stringa
                cleaned_data.append(value)
    
    return cleaned_data

# Configurazione del Consumer Kafka
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id='stazioni-consumer-group',
    key_deserializer=lambda x: x.decode('utf-8'),
    value_deserializer=lambda x: x.decode('utf-8')
)

# Connessione a Cassandra
session = get_cassandra_connection()

# Consumer Kafka: ascolta i messaggi e processa
print(f"Consumer in esecuzione, ascoltando il topic '{KAFKA_TOPIC}'...")

for message in consumer:
    try:
        # Decodifica il messaggio, i dati sono separati da ";"
        file_name = message.key  # Nome del file dal producer
        row_data = message.value.split(";")  # Separiamo i dati con ";"

        # Puliamo e validiamo i dati
        cleaned_data = validate_and_clean_data(row_data)

        # Verifica che i dati siano validi (non None)
        if cleaned_data:
            # Crea la tabella se non esiste già
            create_table(session, file_name)

            # Inserisci i dati nella tabella
            insert_data(session, file_name, cleaned_data)
        else:
            print(f"Dati non validi ricevuti: {message.value}")

    except Exception as e:
        print(f"Errore nel processing del messaggio: {message.value}")
        print(e)
