#inicio treinamento

#inicializando as libs

# Inicio treinamento

# Inicializando as libs
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create a Spark session
spark = SparkSession.builder \
    .appName("MySparkApplication") \
    .getOrCreate()

# Now you can use spark to read data, create DataFrames, etc.
# For example:
# df = spark.read.csv("path/to/your/file.csv", header=True, inferSchema=True)

# Your Spark code goes here

# Don't forget to stop the Spark session when you're done
spark.stop()

