from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession  # Crea una sessione Spark

# Crea la sessione Spark
spark = SparkSession.builder.appName("TimeSeriesPrediction").getOrCreate()

# Carica i dati in un DataFrame
data = spark.read.csv("data.csv", header=True, inferSchema=True)

# Pre-elabora i dati (ad esempio, creare colonne per l'anno, mese, giorno, ecc.)
# Assicurati che i tuoi dati abbiano una colonna 'timestamp' e una colonna 'value'

# Creazione delle caratteristiche (features)
from pyspark.ml.feature import VectorAssembler
assembler = VectorAssembler(inputCols=["timestamp"], outputCol="features")
data = assembler.transform(data)

# Dividi i dati in set di addestramento e test
train_data, test_data = data.randomSplit([0.8, 0.2])

# Crea e addestra il modello di regressione lineare
lr = LinearRegression(featuresCol="features", labelCol="LIVELLO IDROMETRICO")
lr_model = lr.fit(train_data)

# Fai delle previsioni
predictions = lr_model.transform(test_data)

# Mostra le previsioni
predictions.select("timestamp", "value", "prediction").show()
