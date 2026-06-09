import pandas as pd
import numpy as np
from linearmodels.iv import IV2SLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO SELEÇÃO DE LAGS (AIC/BIC) PARA 2SLS ===")

# 1. Carregamento e Preparação
arquivo = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_2sls_investimento.csv'
df = pd.read_csv(arquivo)

df['Period'] = pd.to_datetime(df['Period'])
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# 2. Geração do Instrumento
df['Instrumento_Bartik'] = df['Share_2012q1'] * df['d_ln_PPI_Semi']

# 3. Engenharia de Defasagens (0 a 4 lags)
print("Gerando defasagens para Endógena e Instrumento...")
for i in range(1, 5):
    df[f'Impacto_tech_setor_lag{i}'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(i)
    df[f'Instrumento_Bartik_lag{i}'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(i)

df['const'] = 1

# 4. Amostra Fixa (CRÍTICO)
vars_all = [
    'd_ln_Produtividade', 'const', 'd_ln_Cambio', 'VAB_Industria_Volume',
    'Impacto_tech_setor', 'Impacto_tech_setor_lag1', 'Impacto_tech_setor_lag2', 'Impacto_tech_setor_lag3', 'Impacto_tech_setor_lag4',
    'Instrumento_Bartik', 'Instrumento_Bartik_lag1', 'Instrumento_Bartik_lag2', 'Instrumento_Bartik_lag3', 'Instrumento_Bartik_lag4'
]

df_model = df[vars_all].dropna()
N = len(df_model)
print(f"Matriz de Estimação Universal pronta com N={N} observações.")

# 5. Loop de Estimação
resultados = []

exog_vars = ['const', 'd_ln_Cambio', 'VAB_Industria_Volume']
dependent = df_model['d_ln_Produtividade']

print("\nExecutando Otimização...")
for k in range(5):
    # Definir listas de variáveis
    if k == 0:
        endog_vars = ['Impacto_tech_setor']
        inst_vars = ['Instrumento_Bartik']
    else:
        endog_vars = ['Impacto_tech_setor'] + [f'Impacto_tech_setor_lag{i}' for i in range(1, k+1)]
        inst_vars = ['Instrumento_Bartik'] + [f'Instrumento_Bartik_lag{i}' for i in range(1, k+1)]
        
    exog = df_model[exog_vars]
    endog = df_model[endog_vars]
    instruments = df_model[inst_vars]
    
    # Rodar IV2SLS
    mod = IV2SLS(dependent=dependent, exog=exog, endog=endog, instruments=instruments)
    res = mod.fit(cov_type='kernel')
    
    # Cálculos Manuais de AIC/BIC
    ssr = np.sum(res.resids**2)
    p = len(exog_vars) + len(endog_vars) # Número de parâmetros estimados no segundo estágio
    
    aic = N * np.log(ssr/N) + 2 * p
    bic = N * np.log(ssr/N) + p * np.log(N)
    
    # Extração do menor F (Primeiro Estágio)
    try:
        f_vals = []
        for endog_name in endog_vars:
            # res.first_stage.diagnostics tem colunas para cada endogena
            val = res.first_stage.diagnostics[endog_name].loc['Partial F-statistic']
            f_vals.append(val)
        min_f = np.min(f_vals)
    except Exception as e:
        print(f"Error extracting F-stat at lag {k}: {e}")
        min_f = np.nan
        
    resultados.append({
        'Lags': k,
        'Menor_F_1o_Estagio': min_f,
        'AIC': aic,
        'BIC': bic
    })

# 6. Output Final
df_res = pd.DataFrame(resultados).set_index('Lags')

print("\n--- CRITÉRIOS DE INFORMAÇÃO E INSTRUMENTOS (Amostra Constante) ---")
print(df_res)

melhor_aic = df_res['AIC'].idxmin()
melhor_bic = df_res['BIC'].idxmin()

print(f"\nConclusão:")
print(f"O Critério AIC minimiza com: {melhor_aic} lag(s)")
print(f"O Critério BIC minimiza com: {melhor_bic} lag(s)")
