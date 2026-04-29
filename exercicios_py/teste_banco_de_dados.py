import sqlite3
import pandas as pd
import os

# ==================== NOVA CONEXÃO LIMPA ====================
nome_db = "cadastro_estudantes.db"

print(" Diretório atual:", os.getcwd())
print(" Arquivo encontrado?", os.path.exists(nome_db))
print(" Caminho completo:", os.path.abspath(nome_db))

# Cria uma conexão nova
conn = sqlite3.connect(nome_db)
print(" Conexão criada com sucesso!\n")

# Verifica as tabelas
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
print("📋 Tabelas no banco:", tabelas)

# ====================== LEITURA ======================
query = "SELECT * FROM tb_alunos"
df_aluno = pd.read_sql(query, conn)

print("\n Sucesso! Linhas carregadas:", len(df_aluno))
print(df_aluno.head())