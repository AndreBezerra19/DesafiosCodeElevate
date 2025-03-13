import duckdb

# Conectar ao banco de dados
con = duckdb.connect("/app/desafios.duckdb")

# Mostrar todas as tabelas do primeiro schema
print("\n🗂️ Tabelas no schema 'sensor_monitor':")
print(con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'sensor_monitor'").fetchall())

# Mostrar todas as tabelas do segundo schema
print("\n🗂️ Tabelas no schema 'diario_de_bordo':")  # Troque pelo nome correto do schema
print(con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'diario_de_bordo'").fetchall())

# Fechar conexão
con.close()