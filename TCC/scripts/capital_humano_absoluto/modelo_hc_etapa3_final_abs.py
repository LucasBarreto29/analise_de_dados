import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO MODELO HC ETAPA 3 FINAL: 2 LAGS (ESTOQUE ABSOLUTO / AIC OTIMIZADO) ===")

# 1. Preparação e Trava de Segurança
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_capital_humano_completo.csv')
df['Capital_Humano_FGV'] = pd.to_numeric(df['Capital_Humano_FGV'], errors='coerce')

df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# 2. Transformações Logarítmicas
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Capital_FGV'] = np.log(df['Capital_Humano_FGV'])
df['ln_Estoque_TI'] = np.log(df['Estoque_TI_Setor'])
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# 3. Diferenças (Taxas de Crescimento Percentual)
df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Capital_FGV'] = df.groupby(level='Setor')['ln_Capital_FGV'].diff()
df['d_Selic'] = df.groupby(level='Setor')['Selic'].diff()
df['d_ln_Estoque_TI'] = df.groupby(level='Setor')['ln_Estoque_TI'].diff()

# 4. Lags (2 Lags conforme minimização do AIC)
df['d_ln_Estoque_TI_lag1'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(1)
df['d_ln_Estoque_TI_lag2'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(2)

# 5. Matriz de Estimação
df['const'] = 1

vars_model = [
    'd_ln_Produtividade', 'd_ln_Estoque_TI', 
    'd_ln_Estoque_TI_lag1', 'd_ln_Estoque_TI_lag2',
    'd_Selic', 'd_ln_Capital_FGV', 'const'
]
df_model = df[vars_model].dropna()

# 6. Estimação Robusta
exog_vars = ['const', 'd_ln_Estoque_TI', 'd_ln_Estoque_TI_lag1', 'd_ln_Estoque_TI_lag2', 'd_Selic', 'd_ln_Capital_FGV']
mod = PanelOLS(df_model['d_ln_Produtividade'], df_model[exog_vars], entity_effects=False)
res = mod.fit(cov_type='kernel')

print("\n================================================================================")
print("     RESULTADO ETAPA 3: MODELO FINAL HC (2 LAGS - ESTOQUE ABSOLUTO DE TI)       ")
print("================================================================================")
print(res.summary)

# 7. Teste de Hipótese (Wald)
wald_formula = 'd_ln_Estoque_TI + d_ln_Estoque_TI_lag1 + d_ln_Estoque_TI_lag2 = 0'
wald_test = res.wald_test(formula=wald_formula)

print("\n================================================================================")
print("               TESTE DE WALD (EFEITO LÍQUIDO EM 1 SEMESTRE)                     ")
print("================================================================================")
print("Hipótese Nula (H0): O efeito acumulado (Contemporâneo + 2 Lags) é zero.")
print(f"Estatística F: {wald_test.stat:.4f}")
print(f"p-valor:       {wald_test.pval:.4f}")

if wald_test.pval < 0.05:
    print("\nConclusão: Rejeitamos H0. O impacto líquido ao longo de 1 semestre é estatisticamente diferente de zero.")
else:
    print("\nConclusão: Não rejeitamos H0. O impacto líquido acumulado é estatisticamente nulo ao final de 1 semestre.")
