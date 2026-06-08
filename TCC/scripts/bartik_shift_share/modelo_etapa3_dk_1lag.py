import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO ETAPA 3: MODELO DRISCOLL-KRAAY (1 LAG) E SELEÇÃO DE LAGS ===")

# 1. Carregamento e Transformação Básica
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_bartik.csv')
df = df.dropna(subset=['Bartik_Tech_it']).copy()
df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period'])

df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Bartik_Tech'] = np.log(df['Bartik_Tech_it'])

df['d_ln_Produtividade'] = df.groupby(level='Setor')['ln_Produtividade'].diff()
df['d_ln_Bartik_Tech'] = df.groupby(level='Setor')['ln_Bartik_Tech'].diff()

# Criar Lag 1
df['d_ln_Bartik_Tech_lag1'] = df.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(1)

# Base para o Modelo 1 Lag
df_1lag = df.dropna(subset=['d_ln_Produtividade', 'd_ln_Bartik_Tech', 'd_ln_Bartik_Tech_lag1']).copy()
df_1lag['const'] = 1

# 2. Estimação do Modelo 3 (1 Lag + Driscoll-Kraay)
exog_vars_1lag = ['const', 'd_ln_Bartik_Tech', 'd_ln_Bartik_Tech_lag1', 'VAB_Industria_Volume', 'Stringency_Index']
mod_dk = PanelOLS(df_1lag['d_ln_Produtividade'], df_1lag[exog_vars_1lag], entity_effects=False)
res_dk = mod_dk.fit(cov_type='kernel')

print("\n=== SUMMARY DO MODELO EM PRIMEIRA DIFERENÇA COM DRISCOLL-KRAAY (1 LAG) ===")
print(res_dk.summary)

# 3. Rotina de Seleção do Número Ótimo de Lags (AIC / BIC)
print("\n--- ROTINA DE SELEÇÃO ÓTIMA DE LAGS (CRITÉRIOS DE INFORMAÇÃO) ---")
# Criar cópia para os 4 lags
df_lags = df.copy()

df_lags['d_ln_Bartik_Tech_lag2'] = df_lags.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(2)
df_lags['d_ln_Bartik_Tech_lag3'] = df_lags.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(3)
df_lags['d_ln_Bartik_Tech_lag4'] = df_lags.groupby(level='Setor')['d_ln_Bartik_Tech'].shift(4)

cols_lags = [
    'd_ln_Produtividade', 'd_ln_Bartik_Tech', 
    'd_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2', 
    'd_ln_Bartik_Tech_lag3', 'd_ln_Bartik_Tech_lag4',
    'VAB_Industria_Volume', 'Stringency_Index'
]

# DROPNA GERAL para garantir que TODOS os modelos usem exatamente a MESMA amostra
df_lags = df_lags.dropna(subset=cols_lags).copy()
df_lags['const'] = 1

print(f"Tamanho da amostra balanceada para o teste: {len(df_lags)} observações.")

base_exog = ['const', 'd_ln_Bartik_Tech']
lags_to_add = ['d_ln_Bartik_Tech_lag1', 'd_ln_Bartik_Tech_lag2', 'd_ln_Bartik_Tech_lag3', 'd_ln_Bartik_Tech_lag4']
controls = ['VAB_Industria_Volume', 'Stringency_Index']

results_table = []

for i in range(1, 5):
    # Selecionar variáveis de lag até o lag i
    current_lags = lags_to_add[:i]
    current_exog = base_exog + current_lags + controls
    
    mod = PanelOLS(df_lags['d_ln_Produtividade'], df_lags[current_exog], entity_effects=False)
    # Ajuste simples, os resíduos e loglik não dependem do tipo de covariância
    res = mod.fit()
    
    # AIC = -2*LogLik + 2*k
    # BIC = -2*LogLik + k*ln(N)
    loglik = res.loglik
    k = len(current_exog)
    N = res.nobs
    
    # linearmodels pode ter .aic e .bic se não tivermos computamos manualmente
    aic = getattr(res, 'aic', -2 * loglik + 2 * k)
    bic = getattr(res, 'bic', -2 * loglik + k * np.log(N))
    
    results_table.append({
        'Modelo': f'{i} Lag(s)',
        'AIC': aic,
        'BIC': bic
    })

# Formatar a tabela
df_results = pd.DataFrame(results_table)
df_results.set_index('Modelo', inplace=True)

print("\nResultados dos Critérios de Informação (Valores Menores indicam Melhor Ajuste):")
print(df_results.to_string())

# Identificar o vencedor
melhor_aic = df_results['AIC'].idxmin()
melhor_bic = df_results['BIC'].idxmin()

print(f"\n--- CONCLUSÃO DA SELEÇÃO DE LAGS ---")
print(f"Modelo sugerido pelo critério AIC: {melhor_aic}")
print(f"Modelo sugerido pelo critério BIC: {melhor_bic}")
