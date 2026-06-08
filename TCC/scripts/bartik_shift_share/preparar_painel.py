import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

print("Iniciando a preparação do Painel de Dados...\n")

# ==========================================
# 1. DADOS DA FGV (PRODUTIVIDADE - Y)
# ==========================================
print("Carregando FGV (Produtividade por hora habitual)...")
caminho_fgv = "dados/indicadores_trimestrais_de_produtividade_do_trabalho_4t2025 - cópia.xlsx"
df_fgv = pd.read_excel(caminho_fgv, sheet_name="prod. por hora habitual", header=8)

# Remover linhas vazias no início ou fim
df_fgv = df_fgv.dropna(subset=['Data']).copy()

# Filtrar as colunas dos 7 subsetores de serviços
colunas_servicos_fgv = [
    'Comércio', 
    'Transporte', 
    'Serviço de Informação', 
    'Intermediação Financeira', 
    'Serviços Imobiliários', 
    'Outros Serviços', 
    'APU'
]
df_fgv_filtrado = df_fgv[['Data'] + colunas_servicos_fgv].copy()
df_fgv_filtrado = df_fgv_filtrado.rename(columns={'Data': 'Trimestre'})

# Converter para formato Longo (Painel)
df_fgv_long = df_fgv_filtrado.melt(
    id_vars=['Trimestre'], 
    value_vars=colunas_servicos_fgv,
    var_name='Setor', 
    value_name='Produtividade_Hora_Habitual'
)

# ==========================================
# 2. DADOS DO IBGE (VAB - CONTROLE)
# ==========================================
print("Carregando IBGE (VAB das Contas Nacionais)...")
df_vab = pd.read_csv("dados/vab_servicos_ibge.csv")

# O formato Trimestre_Cod do IBGE é "YYYYQQ" (ex: 201201 para 1º trimestre)
# A FGV usa "YYYYqX" (ex: 2012q1). Vamos converter o IBGE para o padrão da FGV.
def converter_trimestre_ibge(trim_cod):
    ano = str(trim_cod)[:4]
    tri = str(trim_cod)[-2:]
    return f"{ano}q{int(tri)}"

df_vab['Trimestre'] = df_vab['Trimestre_Cod'].apply(converter_trimestre_ibge)

# Dicionário de mapeamento para igualar os nomes dos setores do IBGE aos da FGV
mapa_setores = {
    'Comércio': 'Comércio',
    'Transporte, armazenagem e correio': 'Transporte',
    'Informação e comunicação': 'Serviço de Informação',
    'Atividades financeiras, de seguros e serviços relacionados': 'Intermediação Financeira',
    'Atividades imobiliárias': 'Serviços Imobiliários',
    'Outras atividades de serviços': 'Outros Serviços',
    'Administração, defesa, saúde e educação públicas e seguridade social': 'APU',
    'Administração, saúde e educação públicas e seguridade social': 'APU' # Variação do nome na API
}

df_vab['Setor'] = df_vab['Setor_Nome'].map(mapa_setores)

# Mantendo apenas os dados de VAB mapeados
df_vab_limpo = df_vab[['Trimestre', 'Setor', 'VAB_Indice_Volume']].copy()
# Remover eventuais nulos (setores que não mapearam)
df_vab_limpo = df_vab_limpo.dropna(subset=['Setor'])

# ==========================================
# 3. DADOS COMEX STAT (CHOQUE TECNOLÓGICO - X)
# ==========================================
print("Carregando Comex Stat (Choque Tecnológico)...")
df_comex = pd.read_csv("dados/comex_tech_importacoes.csv")

# Criar o Trimestre_Cod da mesma forma (YYYYqX)
# Trimestre 1 = Meses 1,2,3 / Tri 2 = 4,5,6 / etc
df_comex['Trimestre'] = df_comex['Ano'].astype(str) + 'q' + ((df_comex['Mes'] - 1) // 3 + 1).astype(str)

# Agrupar mensal para trimestral
df_comex_tri = df_comex.groupby('Trimestre')['Investimento_Tech_USD'].sum().reset_index()

# ==========================================
# 4. O GRANDE MERGE (FUSÃO DO PAINEL)
# ==========================================
print("Fundindo as bases (Merge)...")

# 1. Juntar Produtividade com VAB (Ligação por Trimestre E Setor)
painel = pd.merge(df_fgv_long, df_vab_limpo, on=['Trimestre', 'Setor'], how='inner')

# 2. Juntar com o Choque Tech Macro (Ligação APENAS por Trimestre, será copiado para todos os setores)
painel = pd.merge(painel, df_comex_tri, on='Trimestre', how='inner')

# Ordenar lindamente
painel = painel.sort_values(by=['Setor', 'Trimestre']).reset_index(drop=True)

# Salvar
caminho_saida = "dados/painel_mestre.csv"
painel.to_csv(caminho_saida, index=False)

print("\n✅ PAINEL MESTRE CRIADO COM SUCESSO!")
print(f"-> Salvo em: {caminho_saida}")
print(f"-> Total de linhas: {len(painel)} (Esperado: 7 setores * ~56 trimestres = ~392)")
print("\nAmostra dos dados:")
print(painel.head(10))
