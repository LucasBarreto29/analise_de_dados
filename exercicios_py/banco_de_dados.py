import sqlite3
import pandas as pd
import os

# Banco de dados SQLite
nome_db = "cadastro_estudantes.db"

print(" Diretório atual:", os.getcwd())
print(" Arquivo encontrado?", os.path.exists(nome_db))
print(" Caminho completo:", os.path.abspath(nome_db))

# Cria a conexão com o banco de dados
conn = sqlite3.connect(nome_db)
print(" Conexão criada com sucesso!\n")

# Verifica as tabelas
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
print("Tabelas no banco:", tabelas)

# Trazer para dentro do pandas
query = "SELECT * FROM tb_alunos"
df_aluno = pd.read_sql(query, conn)

print("\n Sucesso! Linhas carregadas:", len(df_aluno))
print(df_aluno)

query = "SELECT * FROM tb_enderecos"
df_endereco = pd.read_sql(query, conn)

# Merge entre tb_alunos e tb_enderecos

df = pd.merge(df_aluno, df_endereco, left_on = "endereco_id", right_on= "id", how="inner")
df[["nome_aluno", "email", "endereco"]]
