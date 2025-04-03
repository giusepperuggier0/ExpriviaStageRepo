from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, to_timestamp, minute, date_format, floor, avg, round, concat, lit, concat_ws


POSTGRES_USER = "hive"  
POSTGRES_PASSWORD = "password"  
POSTGRES_DB = "postgres"  
POSTGRES_HOST = "localhost"  
POSTGRES_PORT = "5432"


spark = SparkSession.builder \
    .appName("CaricamentoDatiPostgres") \
    .config("spark.jars", "file:///C:/Users/Giuseppe/Downloads/postgresql-42.7.5.jar") \
    .getOrCreate()


cartella_dati = "C:/Users/Giuseppe/Desktop/Stage_exprivia/Python/Analisi_livello_marino_adriatico"
mesi = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO"]

df_list = []

for mese in mesi:
    file_path = f"{cartella_dati}/BARI_{mese}.csv"
    df = spark.read.option("delimiter", ";").option("header", True).csv(file_path)

    for col_name in ["LIVELLO IDROMETRICO", "TEMPERATURA ARIA", "UMIDITÀ RELATIVA", "PRESSIONE ATMOSFERICA"]:
        df = df.withColumn(col_name, regexp_replace(col(col_name), ",", ".").cast("double"))

    df = df.withColumn("DATA_ORA", to_timestamp(concat_ws(" ", col("DATA"), col("ORA")), "yyyy-MM-dd HH:mm"))
    df = df.filter(minute(col("DATA_ORA")).isin([0, 10, 20, 30, 40, 50]))

    df_hourly = df.groupBy(floor(col("DATA_ORA").cast("long") / 3600).alias("ora"))
    df_hourly = df_hourly.agg(
        avg("LIVELLO IDROMETRICO").alias("LIVELLO IDROMETRICO"),
        avg("TEMPERATURA ARIA").alias("TEMPERATURA ARIA"),
        avg("PRESSIONE ATMOSFERICA").alias("PRESSIONE ATMOSFERICA"),
        avg("UMIDITÀ RELATIVA").alias("UMIDITÀ RELATIVA")
    )

    df_hourly = df_hourly.withColumn("DATA_ORA", (col("ora") * 3600).cast("timestamp"))
    df_hourly = df_hourly.withColumn("DATA", date_format(col("DATA_ORA"), "yyyy-MM-dd"))
    df_hourly = df_hourly.withColumn("ORA", date_format(col("DATA_ORA"), "HH:mm"))

    df_hourly = df_hourly.select("DATA", "ORA", "LIVELLO IDROMETRICO", "TEMPERATURA ARIA", "PRESSIONE ATMOSFERICA", "UMIDITÀ RELATIVA")
    df_list.append(df_hourly)

df_finale = df_list[0]
for df in df_list[1:]:
    df_finale = df_finale.union(df)


df_finale = df_finale.withColumn("LIVELLO IDROMETRICO", round(col("LIVELLO IDROMETRICO"), 3)) \
    .withColumn("TEMPERATURA ARIA", round(col("TEMPERATURA ARIA"), 1)) \
    .withColumn("PRESSIONE ATMOSFERICA", round(col("PRESSIONE ATMOSFERICA"), 1)) \
    .withColumn("UMIDITÀ RELATIVA", round(col("UMIDITÀ RELATIVA"), 1))

df_finale = df_finale.orderBy(["DATA", "ORA"])


jdbc_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
properties = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}

df_finale.write \
    .jdbc(url=jdbc_url, table="livello_marino", mode="overwrite", properties=properties)

print("Dati caricati con successo su PostgreSQL!")