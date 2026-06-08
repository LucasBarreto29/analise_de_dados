import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO SELEÇÃO DE LAGS (AIC/BIC) PARA ESTOQUE ABSOLUTO DE TI ===")

# 1. Preparação
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_capital_humano_completo.csv')
df['Capital_Humano_FGV'] = pd.to_numeric(df['Capital_Humano_FGV'], errors='coerce')

df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# Transformações Logarítmicas
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Capital_FGV'] = np.log(df['Capital_Humano_FGV'])
# APLICAÇÃO DO LOGARITMO NO ESTOQUE ABSOLUTO ANTES DA DIFERENÇA
df['ln_Estoque_TI'] = np.log(df['Estoque_TI_Setor'])
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Diferenças
df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Capital_FGV'] = df.groupby(level='Setor')['ln_Capital_FGV'].diff()
df['d_Selic'] = df.groupby(level='Setor')['Selic'].diff()
# CRESCIMENTO PERCENTUAL ABSOLUTO
df['d_ln_Estoque_TI'] = df.groupby(level='Setor')['ln_Estoque_TI'].diff()

# Lags
df['d_ln_Estoque_TI_lag1'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(1)
df['d_ln_Estoque_TI_lag2'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(2)
df['d_ln_Estoque_TI_lag3'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(3)
df['d_ln_Estoque_TI_lag4'] = df.groupby(level='Setor')['d_ln_Estoque_TI'].shift(4)

# 2. Criar a base restrita (Constante Sample Size) para comparar AIC/BIC
df['const'] = 1
vars_all = [
    'd_ln_Produtividade', 'd_ln_Estoque_TI', 
    'd_ln_Estoque_TI_lag1', 'd_ln_Estoque_TI_lag2',
    'd_ln_Estoque_TI_lag3', 'd_ln_Estoque_TI_lag4',
    'd_Selic', 'd_ln_Capital_FGV', 'const'
]
df_model = df[vars_all].dropna()

# 3. Loop de Seleção
resultados = []

for lags in range(1, 5):
    # Selecionar as defasagens corretas
    exog_vars = ['const', 'd_ln_Estoque_TI', 'd_Selic', 'd_ln_Capital_FGV']
    for i in range(1, lags + 1):
        exog_vars.append(f'd_ln_Estoque_TI_lag{i}')
    
    Y = df_model['d_ln_Produtividade']
    X = df_model[exog_vars]
    
    # Rodar Pooled OLS (statsmodels)
    mod = sm.OLS(Y, X)
    res = mod.fit()
    
    resultados.append({
        'Lags': lags,
        'AIC': res.aic,
        'BIC': res.bic,
        'R2': res.rsquared
    })

# Converter para DataFrame e exibir
df_res = pd.DataFrame(resultados).set_index('Lags')
print("\n--- CRITÉRIOS DE INFORMAÇÃO (Amostra Constante: N={}) ---".format(len(df_model)))
print(df_res)

melhor_aic = df_res['AIC'].idxmin()
melhor_bic = df_res['BIC'].idxmin()

print(f"\nConclusão:")
print(f"O Critério AIC minimiza com: {melhor_aic} lag(s)")
print(f"O Critério BIC minimiza com: {melhor_bic} lag(s)")
