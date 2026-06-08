import sidrapy
import pandas as pd
import os

print("Conectando à API do IBGE (SIDRA) para baixar a Tabela 5932...")
print("Isso pode levar alguns segundos...")

try:
    # Baixa a tabela 5932 (Série encadeada do índice de volume trimestral - VAB)
    # variable = 6564
    # classifications={"11255": "all"} -> Puxa todas as atividades econômicas
    df_raw = sidrapy.get_table(
        table_code="5932",
        territorial_level="1",
        ibge_territorial_code="all",
        variable="6564",
        period="all",
        classifications={"11255": "all"}
    )
    
    # Substituir os nomes das colunas pelos valores da primeira linha (que o SIDRA retorna como cabeçalho legível)
    df_raw.columns = df_raw.iloc[0]
    df = df_raw.iloc[1:].reset_index(drop=True)
    
    # Vamos padronizar o nome das colunas caso o IBGE mude letras maiúsculas/minúsculas
    col_mapping = {
        'Trimestre (Código)': 'Trimestre_Cod',
        'Setores e subsetores (Código)': 'Setor_Cod',
        'Setores e subsetores': 'Setor_Nome',
        'Valor': 'VAB_Indice_Volume'
    }
    
    # Renomear de forma segura (pegando colunas que contenham essas palavras chave)
    for col in df.columns:
        if 'Trimestre (Código)' in col or 'Trimestre (código)' in col:
            df.rename(columns={col: 'Trimestre_Cod'}, inplace=True)
        elif 'Setores e subsetores (Código)' in col or 'Setores e subsetores (código)' in col:
            df.rename(columns={col: 'Setor_Cod'}, inplace=True)
        elif 'Setores e subsetores' in col:
            df.rename(columns={col: 'Setor_Nome'}, inplace=True)
        elif 'Valor' == col:
            df.rename(columns={col: 'VAB_Indice_Volume'}, inplace=True)
            
    df_clean = df[['Trimestre_Cod', 'Setor_Cod', 'Setor_Nome', 'VAB_Indice_Volume']].copy()
    
    # 1. Filtrar o tempo: Apenas 2012 em diante (Formato: YYYYQQ, ex: 201201)
    df_clean = df_clean[df_clean['Trimestre_Cod'] >= '201201']
    
    # 2. Filtrar apenas os 7 Subsetores de Serviços que compõem o nosso Painel
    # Códigos oficiais do IBGE na classificação 11255:
    codigos_servicos = [
        '90697', # Comércio
        '90698', # Transporte, armazenagem e correio
        '90699', # Informação e comunicação
        '90700', # Atividades financeiras, de seguros e serviços relacionados
        '90702', # Atividades imobiliárias
        '90701', # Outras atividades de serviços
        '90703'  # Administração, defesa, saúde e educação públicas
    ]
    
    df_servicos = df_clean[df_clean['Setor_Cod'].isin(codigos_servicos)].copy()
    
    # Converter o valor para numérico
    df_servicos['VAB_Indice_Volume'] = pd.to_numeric(df_servicos['VAB_Indice_Volume'], errors='coerce')
    
    # Criar a pasta dados se não existir
    os.makedirs("dados", exist_ok=True)
    
    # Salvar o CSV
    caminho_saida = "dados/vab_servicos_ibge.csv"
    df_servicos.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
    
    print("\n✅ Sucesso! O arquivo foi gerado perfeitamente.")
    print(f"Caminho do arquivo: {caminho_saida}")
    print(f"Total de linhas extraídas: {len(df_servicos)}")
    print("\nVisualização das primeiras linhas:")
    print(df_servicos.head())

except Exception as e:
    print(f"\n❌ Erro ao puxar os dados: {e}")
