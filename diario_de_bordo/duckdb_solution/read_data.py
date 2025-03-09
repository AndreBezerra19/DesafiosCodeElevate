# Dependencies
import duckdb
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring, count, col, when, desc, min, max, sum, round, to_date, date_format

# Parameters
db_path = "/Users/andrebezerra/Desktop/Dev/DesafiosCodeElevate/db_desafios.duckdb"
table_name = "b_info_transportes"
schema = "diario_de_bordo"

# Database connection
con = duckdb.connect(db_path)

# Read table using pandas
df = con.execute(f"SELECT * FROM {schema}.{table_name}").fetchdf()

# date information and conversion
df["DATA_INICIO"] = df["DATA_INICIO"].str.split(" ").str[0]  # get only date
df["DATA_INICIO"] = pd.to_datetime(df["DATA_INICIO"], format="%m-%d-%Y").dt.strftime("%Y-%m-%d")

con.close()

##### ETL #####

# Spark session
spark = SparkSession.builder.appName("DuckDB_PySpark").getOrCreate()

# Converter o DataFrame Pandas para PySpark
df_spark = spark.createDataFrame(df)

# data aggregation
df_resultado = df_spark.groupBy("DATA_INICIO").agg(
    count(col("LOCAL_INICIO")).alias("QT_CORR"),        # total travels
    count(when(col("CATEGORIA") == "Negocio", True)).alias("QT_CORR_NEG"),      # Count travels like 'Negocio'
    count(when(col("CATEGORIA") == "Pessoal", True)).alias("QT_CORR_PESS"),     # Count travels like 'Pessoal'
    max(col("DISTANCIA")).alias("VL_MAX_DIST"),     # longest distance of the day
    min(col("DISTANCIA")).alias("VL_MIN_DIST"),     # shortest distance of the day
    round(sum(col("DISTANCIA")) / count(col("DATA_INICIO")), 2).alias("VL_AVG_DIST"),       # average total distance
    count(when(col("PROPOSITO").isin("Reunião"), True)).alias("QT_CORR_REUNI"),     # Travels for the purpose of "Reunião".
    count(when((col("PROPOSITO").isNotNull()) & (~col("PROPOSITO").isin("Reunião")), True)).alias("QT_CORR_NAO_REUNI")      # Travels with a stated purpose other than "Reunião".  
).orderBy(col("DATA_INICIO").desc())

# Save into DuckDB on correct schema
pd_resultados = df_resultado.toPandas()
con = duckdb.connect(db_path)

# Create table
con.execute("""
    CREATE TABLE IF NOT EXISTS diario_de_bordo.s_info_corridas_do_dia (
        DATA_INICIO DATE,
        QT_CORR INTEGER,
        QT_CORR_NEG INTEGER,
        QT_CORR_PESS INTEGER,
        VL_MAX_DIST FLOAT,
        VL_MIN_DIST FLOAT,
        VL_AVG_DIST FLOAT,
        QT_CORR_REUNI INTEGER,
        QT_CORR_NAO_REUNI INTEGER
    )
""")

con.register("temp_table", pd_resultados)  # Register DF like temp table

# insert data into table
con.execute("""
    INSERT INTO diario_de_bordo.s_info_corridas_do_dia 
    SELECT * FROM temp_table
""")

con.close()

print("Table saved successfully in DuckDB! 🚀")