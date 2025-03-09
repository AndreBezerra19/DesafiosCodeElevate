# Dependencies
import duckdb
import pandas as pd

# Paths
file_path = "/Users/andrebezerra/Desktop/Dev/DesafiosCodeElevate/diario_de_bordo/info_transportes.csv"
db_path = "/Users/andrebezerra/Desktop/Dev/DesafiosCodeElevate/db_desafios.duckdb"

# Read file
transportes = pd.read_csv(file_path, sep=";")

# Database connection
con = duckdb.connect(db_path)

# Create schema
con.execute("CREATE SCHEMA IF NOT EXISTS diario_de_bordo")

# Save into DuckDB on correct schema
con.register("temp_table", transportes)  # Register DF like temp table
con.execute("CREATE TABLE IF NOT EXISTS diario_de_bordo.b_info_transportes AS SELECT * FROM temp_table")

# Close connection
con.close()
print("Table saved successfully in DuckDB! 🚀")