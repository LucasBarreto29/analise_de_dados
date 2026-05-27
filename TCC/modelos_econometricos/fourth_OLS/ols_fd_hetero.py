"""
FOURTH OLS (Efeitos Heterogêneos) - Quem ganha mais produtividade?
----------------------------------------------------------------------
Este modelo quebra a média nacional e interage o choque de tecnologia (Lag 4)
com as Dummies de cada sub-setor de serviços. O objetivo é criar um ranking
de quais setores conseguem converter tecnologia em produtividade de forma mais
eficiente.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# Configurações de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

# O script subiu um nível, então precisamos de três 'dirname' para chegar na pasta TCC
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------
# 1. CARREGAMENTO E TRANSFORMAÇÃO (DIFERENÇAS + LAGS)
# ---------------------------------------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))
df['ln_Invest_Tech'] = np.log(df['Investimento_Tech_USD'])
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()
df['d_ln_Invest_Tech'] = df.groupby('Setor')['ln_Invest_Tech'].diff()
df['d_VAB_Indice'] = df.groupby('Setor')['VAB_Indice_Volume'].diff()

for i in range(1, 5):
    df[f'd_ln_Invest_Tech_L{i}'] = df.groupby('Setor')['d_ln_Invest_Tech'].shift(i)

df_diff = df.dropna().copy()

print("="*70)
print(" RESULTADOS DO MODELO DE EFEITOS HETEROGÊNEOS (LAG 4 x SETOR) ")
print("="*70)

# O termo "- 1" remove o intercepto global para forçar o statsmodels a 
# estimar um coeficiente explícito de tecnologia para CADA UM dos 7 setores 
# (do contrário, ele usaria um como base e os outros seriam relativos).
formula = 'd_ln_Produtividade ~ d_VAB_Indice + d_ln_Invest_Tech_L4:C(Setor) - 1'

modelo_hetero = smf.ols(
    formula=formula,
    data=df_diff
).fit(cov_type='cluster', cov_kwds={'groups': df_diff['Setor']})

print(modelo_hetero.summary().tables[1])

# ---------------------------------------------------------
# 2. EXTRAÇÃO DOS DADOS PARA O GRÁFICO (RANKING)
# ---------------------------------------------------------
# Filtrando apenas os coeficientes de interação (tecnologia x setor)
resultados = []
for index in modelo_hetero.params.index:
    if "d_ln_Invest_Tech_L4:C(Setor)" in index:
        # Extrair nome do setor limpo. Ex: d_ln_Invest_Tech_L4:C(Setor)[Comércio] -> Comércio
        nome_setor = index.split("[")[1].replace("]", "")
        coef = modelo_hetero.params[index]
        p_val = modelo_hetero.pvalues[index]
        err_padrao = modelo_hetero.bse[index]
        resultados.append({
            'Setor': nome_setor,
            'Coeficiente (%)': coef * 100, # Transformando para impacto percentual
            'P-value': p_val,
            'Significativo': p_val < 0.10,
            'Erro Padrão (%)': err_padrao * 100
        })

df_rank = pd.DataFrame(resultados).sort_values(by='Coeficiente (%)', ascending=False)

print("\n--- RANKING DE ASSIMILAÇÃO TECNOLÓGICA ---")
print(df_rank[['Setor', 'Coeficiente (%)', 'P-value']].to_string(index=False))
print("="*70)

# ---------------------------------------------------------
# 3. GERAÇÃO DO GRÁFICO DE BARRAS
# ---------------------------------------------------------
plt.figure(figsize=(12, 7))

# Definindo cores: Verde para estatisticamente significativo (p<0.10), Cinza para não-significativo
cores = ['#2ca02c' if sig else '#7f7f7f' for sig in df_rank['Significativo']]

ax = sns.barplot(
    x='Coeficiente (%)', 
    y='Setor', 
    data=df_rank, 
    palette=cores,
    edgecolor='black',
    linewidth=1.5
)

# Adicionando a linha do Zero
plt.axvline(0, color='black', linewidth=1.5, linestyle='--')

# Configurando títulos e rótulos
plt.title('Ranking: Qual sub-setor de Serviços\nganha mais Produtividade com a Tecnologia? (Após 1 ano)', 
          fontweight='bold', pad=20, fontsize=16)
plt.xlabel('Impacto na Produtividade para cada 1% de aumento em Tech (%)', fontweight='bold')
plt.ylabel('')

# Anotações para guiar a leitura (Legenda improvisada)
import matplotlib.patches as mpatches
green_patch = mpatches.Patch(color='#2ca02c', label='Significativo (Comprovado Estatisticamente)')
gray_patch = mpatches.Patch(color='#7f7f7f', label='Efeito não claro (Margem de erro inclui o Zero)')
plt.legend(handles=[green_patch, gray_patch], loc='lower right', frameon=True, shadow=True)

plt.tight_layout()

# Salvando a imagem na própria pasta do script
plot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking_setores.png")
plt.savefig(plot_path, dpi=300)
plt.close()

# Copiando para a pasta de artefatos do chat para exibição
artifact_dir = "/Users/lucas/.gemini/antigravity/brain/6aafc3ac-4c80-488c-8f39-21b359f5cbee"
os.system(f"cp '{plot_path}' '{artifact_dir}/'")

print("Gráfico de Ranking gerado com sucesso!")
