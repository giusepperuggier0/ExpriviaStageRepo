from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurazione Cassandra
CASSANDRA_HOST = 'localhost'  # Modifica con il tuo host Cassandra
CASSANDRA_PORT = 9042
KEYSPACE = 'my_space'  # Modifica con il tuo keyspace

# Connessione a Cassandra
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect(KEYSPACE)  # Assicurati che il keyspace sia corretto

# Elenco delle stazioni valide
valid_stations = [
    "anzio_24", "cagliari_24", "napoli_24", "ponza_24", "trieste_24", "vieste_24",
    "bari_24", "civitavecchia_24", "palermo_24", "ravenna_24", "venezia_24"
]

# **NUOVA ROTTA** per ottenere l'elenco delle stazioni
@app.route('/valid_stations', methods=['GET'])
def get_valid_stations():
    return jsonify(valid_stations)

# Rotta per ottenere i dati Kafka
@app.route('/kafka-data', methods=['GET'])
def get_kafka_data():
    station = request.args.get('station')

    if not station:
        return jsonify({"error": "No station provided"}), 400

    # Verifica che la stazione sia valida
    if station not in valid_stations:
        return jsonify({"error": "Invalid station"}), 400

    # Prepara la query in modo sicuro
    query = f"""
    SELECT data, ora, direzione_vento, livello_idrometrico, pressione_atmosferica, 
           temperatura_acqua, temperatura_aria, umidita_relativa, velocita_vento
    FROM {station}
    """
    
    try:
        rows = session.execute(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    data = []
    for row in rows:
        record = {
            'data': row.data,
            'ora': row.ora,
            'direzione_vento': row.direzione_vento or '-',
            'livello_idrometrico': row.livello_idrometrico or '-',
            'pressione_atmosferica': row.pressione_atmosferica or '-',
            'temperatura_acqua': row.temperatura_acqua or '-',
            'temperatura_aria': row.temperatura_aria or '-',
            'umidita_relativa': row.umidita_relativa or '-',
            'velocita_vento': row.velocita_vento or '-'
        }
        data.append(record)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
