import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO MODELO CURVA EM J COM BARTIK FIXO (SHARE 2012q1) ===")

# 1. Carregamento e Preparação do Painel
arquivo_painel = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik_fixo_diff.csv'
df = pd.read_csv(arquivo_painel)

# Configurar o MultiIndex temporal
df['Period'] = pd.to_datetime(df['Period'])
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# 2. Criação das Defasagens (Lags) para a Curva em J
# O instrumento Bartik ('Impacto_tech_setor') já está em primeira diferença
print("Gerando Lags (1 a 4 trimestres)...")
df['Impacto_tech_setor_lag1'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(1)
df['Impacto_tech_setor_lag2'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(2)
df['Impacto_tech_setor_lag3'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(3)
df['Impacto_tech_setor_lag4'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(4)

# 3. Matriz de Estimação
df['const'] = 1

vars_model = [
    'd_ln_Produtividade', 'Impacto_tech_setor', 
    'Impacto_tech_setor_lag1', 'Impacto_tech_setor_lag2',
    'Impacto_tech_setor_lag3', 'Impacto_tech_setor_lag4',
    'd_ln_Cambio', 'VAB_Industria_Volume', 'const'
]

df_model = df[vars_model].dropna()

# 4. Estimação Robusta (Driscoll-Kraay)
exog_vars = [
    'const', 'Impacto_tech_setor', 
    'Impacto_tech_setor_lag1', 'Impacto_tech_setor_lag2',
    'Impacto_tech_setor_lag3', 'Impacto_tech_setor_lag4',
    'd_ln_Cambio', 'VAB_Industria_Volume'
]

print("\nEstimando PanelOLS com matriz de covariância Kernel (Driscoll-Kraay)...")
mod = PanelOLS(df_model['d_ln_Produtividade'], df_model[exog_vars], entity_effects=False)
res = mod.fit(cov_type='kernel')

print("\n================================================================================")
print("       RESULTADO: MODELO DE CURVA EM J (BARTIK SHARE FIXO 2012q1)               ")
print("================================================================================")
print(res.summary)

# 5. Teste de Hipótese (Wald) para o Efeito Líquido Acumulado
wald_formula = 'Impacto_tech_setor + Impacto_tech_setor_lag1 + Impacto_tech_setor_lag2 + Impacto_tech_setor_lag3 + Impacto_tech_setor_lag4 = 0'
wald_test = res.wald_test(formula=wald_formula)

print("\n================================================================================")
print("               TESTE DE WALD (EFEITO LÍQUIDO EM 1 ANO)                          ")
print("================================================================================")
print("Hipótese Nula (H0): O efeito acumulado (Contemporâneo + 4 Lags) é zero.")
print(f"Estatística F: {wald_test.stat:.4f}")
print(f"p-valor:       {wald_test.pval:.4f}")

if wald_test.pval < 0.05:
    print("\nConclusão: Rejeitamos H0. O impacto líquido acumulado da tecnologia após 1 ano é estatisticamente diferente de zero.")
else:
    print("\nConclusão: Não rejeitamos H0. O impacto líquido acumulado da tecnologia após 1 ano é nulo (Paradoxo de Solow Confirmado).")
