# Dependencies
import duckdb
import pandas as pd

# Parameters
db_path = "/Users/andrebezerra/Desktop/Dev/DesafiosCodeElevate/db_desafios.duckdb"
table_name = "b_info_transportes"
schema = "diario_de_bordo"

# Database connection
con = duckdb.connect(db_path)

# Read table using pandas
df = con.execute(f"SELECT * FROM {schema}.{table_name}").fetchdf()

##### ETL #####

# date information and conversion
df["DATA_INICIO"] = df["DATA_INICIO"].str.split(" ").str[0]  # Mantém apenas a data
df["DATA_INICIO"] = pd.to_datetime(df["DATA_INICIO"], format="%m-%d-%Y").dt.strftime("%Y-%m-%d")

# Agrupamento e agregações
df_resultado = df.groupby("DATA_INICIO").agg(
    QT_CORR=pd.NamedAgg(column="LOCAL_INICIO", aggfunc=lambda x: x.notna().sum()),  # Contagem total de viagens (não nulas)
    QT_CORR_NEG=pd.NamedAgg(column="CATEGORIA", aggfunc=lambda x: (x == "Negocio").sum()),  # Contagem de viagens de "Negocio"
    QT_CORR_PESS=pd.NamedAgg(column="CATEGORIA", aggfunc=lambda x: (x == "Pessoal").sum()),  # Contagem de viagens de "Pessoal"
    VL_MAX_DIST=pd.NamedAgg(column="DISTANCIA", aggfunc="max"),  # Maior distância percorrida no dia
    VL_MIN_DIST=pd.NamedAgg(column="DISTANCIA", aggfunc="min"),  # Menor distância percorrida no dia
    VL_AVG_DIST=pd.NamedAgg(column="DISTANCIA", aggfunc=lambda x: round(x.sum() / len(x), 2)),  # Distância média do dia
    QT_CORR_REUNI=pd.NamedAgg(column="PROPOSITO", aggfunc=lambda x: (x == "Reunião").sum()),  # Contagem de viagens para "Reunião"
    QT_CORR_NAO_REUNI=pd.NamedAgg(column="PROPOSITO", aggfunc=lambda x: x.notna().sum() - (x == "Reunião").sum())  # Viagens com propósito diferente de "Reunião"
).reset_index()

# Ordenando os dados do mais recente para o mais antigo
df_resultado = df_resultado.sort_values(by="DATA_INICIO", ascending=False)

# Save into DuckDB on correct schema
con.register("temp_table", df_resultado)  # Register DF like temp table
con.execute("CREATE TABLE IF NOT EXISTS diario_de_bordo.s_info_corridas_do_dia AS SELECT * FROM temp_table")

# Close connection
con.close()
print("Table saved successfully in DuckDB! 🚀")