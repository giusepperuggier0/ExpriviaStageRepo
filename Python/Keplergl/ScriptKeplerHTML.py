from cassandra.cluster import Cluster
import pandas as pd
from keplergl import KeplerGl


CSV_FILE = 'lat_long_stazioniIdrometriche.csv'
KEYSPACE = 'geo_data'
TABLE_NAME = 'citta_costiere'
CASSANDRA_HOSTS = ['127.0.0.1'] 


cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect()


session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
""")


session.set_keyspace(KEYSPACE)


session.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        nome_citta TEXT PRIMARY KEY,
        latitudine DOUBLE,
        longitudine DOUBLE
    )
""")


df = pd.read_csv(CSV_FILE)

insert_query = f"""
    INSERT INTO {TABLE_NAME} (nome_citta, latitudine, longitudine)
    VALUES (%s, %s, %s)
"""

for _, row in df.iterrows():
    session.execute(insert_query, (row['Citta'], row['Latitudine'], row['Longitudine']))


rows = session.execute(f"SELECT nome_citta, latitudine, longitudine FROM {TABLE_NAME}")
data = [{"Citta": r.nome_citta, "Latitudine": r.latitudine, "Longitudine": r.longitudine} for r in rows]
df_map = pd.DataFrame(data)

mappa = KeplerGl(height=600)
mappa.add_data(data=df_map, name='Città costiere')
mappa.save_to_html(file_name='mappa_kepler.html', data={"Città costiere": df_map})


