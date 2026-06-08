import pandas as pd
import ssl
import os
import warnings

# Ignorar alertas de SSL (Erro comum em Macs com Python) e warnings do Pandas
ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings('ignore')

anos = range(2012, 2026)
dfs = []

print("======================================================")
print("Iniciando extração do Comex Stat (Modo Força Bruta)...")
print("Como a API do governo trava muito, este script baixa os")
print("arquivos anuais completos e extrai apenas a Tecnologia.")
print("Pode levar de 1 a 3 minutos. Vá pegar um café! ☕")
print("======================================================\n")

for ano in anos:
    url = f"https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_{ano}.csv"
    try:
        print(f"Baixando e filtrando dados de {ano}...")
        # Lemos apenas as colunas úteis para não estourar a memória RAM (Arquivos de 150MB+)
        colunas_uteis = ['CO_ANO', 'CO_MES', 'CO_NCM', 'VL_FOB']
        df_ano = pd.read_csv(url, sep=';', encoding='latin1', dtype={'CO_NCM': str}, usecols=colunas_uteis)
        
        # Filtro de Ouro: Só NCMs que começam com a nossa "Trindade Tech"
        df_tech = df_ano[df_ano['CO_NCM'].str.startswith(('8471', '8517', '8542'))].copy()
        
        # Como o arquivo é gigantesco, já agrupamos por mês para ficar levinho
        df_agrupado = df_tech.groupby(['CO_ANO', 'CO_MES'])['VL_FOB'].sum().reset_index()
        
        dfs.append(df_agrupado)
        print(f" -> OK! {len(df_tech)} importações de tecnologia encontradas em {ano}.\n")
    except Exception as e:
        print(f" -> Fim da linha no ano {ano} (provavelmente o arquivo ainda não existe). Erro: {e}\n")

print("Juntando 14 anos de dados...")
df_final = pd.concat(dfs, ignore_index=True)

# Renomeando para ficar elegante
df_final = df_final.rename(columns={
    'CO_ANO': 'Ano',
    'CO_MES': 'Mes',
    'VL_FOB': 'Investimento_Tech_USD'
})

# Salvar
os.makedirs("dados", exist_ok=True)
caminho = "dados/comex_tech_importacoes.csv"
df_final.to_csv(caminho, index=False)

print(f"\n✅ SUCESSO ABSOLUTO! Arquivo salvo em: {caminho}")
print(f"Total de meses extraídos: {len(df_final)}")
print(df_final.head())
