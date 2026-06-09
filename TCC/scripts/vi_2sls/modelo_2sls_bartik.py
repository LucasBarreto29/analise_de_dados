import pandas as pd
import numpy as np
from linearmodels.iv import IV2SLS
import warnings
warnings.filterwarnings('ignore')

print("=== INICIANDO MODELO 2SLS (VARIÁVEIS INSTRUMENTAIS) ===")

# 1. Carregamento do Painel
arquivo = '/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_2sls_investimento.csv'
df = pd.read_csv(arquivo)

# Garantir MultiIndex para ordenação correta das defasagens
df['Period'] = pd.to_datetime(df['Period'])
df = df.set_index(['Setor', 'Period'])
df = df.sort_index()

# 2. BLOCO 13A: A Criação do Instrumento Interagido (Z_it)
print("Engenharia de Variáveis Instrumentais e Defasagens...")
# O Instrumento Principal: Vulnerabilidade Histórica x Choque Global de Preços
df['Instrumento_Bartik'] = df['Share_2012q1'] * df['d_ln_PPI_Semi']

# Engenharia das Defasagens da Variável Endógena (Choque_Bartik)
df['Impacto_tech_setor_lag1'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(1)
df['Impacto_tech_setor_lag2'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(2)
df['Impacto_tech_setor_lag3'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(3)
df['Impacto_tech_setor_lag4'] = df.groupby(level='Setor')['Impacto_tech_setor'].shift(4)

# Engenharia das Defasagens do Instrumento (Purificadores)
df['Instrumento_Bartik_lag1'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(1)
df['Instrumento_Bartik_lag2'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(2)
df['Instrumento_Bartik_lag3'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(3)
df['Instrumento_Bartik_lag4'] = df.groupby(level='Setor')['Instrumento_Bartik'].shift(4)

df['const'] = 1

# Limpeza da Matriz Final
vars_todas = [
    'd_ln_Produtividade', 'const', 'd_ln_Cambio', 'VAB_Industria_Volume',
    'Impacto_tech_setor', 'Impacto_tech_setor_lag1', 'Impacto_tech_setor_lag2', 'Impacto_tech_setor_lag3', 'Impacto_tech_setor_lag4',
    'Instrumento_Bartik', 'Instrumento_Bartik_lag1', 'Instrumento_Bartik_lag2', 'Instrumento_Bartik_lag3', 'Instrumento_Bartik_lag4'
]

df_model = df[vars_todas].dropna()

# 3. BLOCO 13B: Estimação com Mínimos Quadrados em Dois Estágios (2SLS)
print(f"Matriz Pronta. Observações válidas: {len(df_model)}")
print("Iniciando Estimação IV2SLS...")

# Variável Dependente (Y)
dependent = df_model['d_ln_Produtividade']

# Variáveis Exógenas (Controles que entram em ambos os estágios)
exog = df_model[['const', 'd_ln_Cambio', 'VAB_Industria_Volume']]

# Variáveis Endógenas (As que sofrem de endogeneidade)
endog = df_model[['Impacto_tech_setor', 'Impacto_tech_setor_lag1', 'Impacto_tech_setor_lag2', 'Impacto_tech_setor_lag3', 'Impacto_tech_setor_lag4']]

# Instrumentos (Os purificadores)
instruments = df_model[['Instrumento_Bartik', 'Instrumento_Bartik_lag1', 'Instrumento_Bartik_lag2', 'Instrumento_Bartik_lag3', 'Instrumento_Bartik_lag4']]

# Inicializar o Modelo 2SLS
iv_model = IV2SLS(dependent=dependent, exog=exog, endog=endog, instruments=instruments)

# Ajustar o Modelo com Correção Robusta (Kernel HAC equivalente ao Driscoll-Kraay)
# Em pooled IV com dependência no tempo, usa-se cov_type='kernel'
iv_res = iv_model.fit(cov_type='kernel')

print("\n================================================================================")
print("                 SUMÁRIO DO MODELO 2SLS (SEGUNDO ESTÁGIO)                       ")
print("================================================================================")
print(iv_res.summary)

print("\n================================================================================")
print("                 DIAGNÓSTICO DO PRIMEIRO ESTÁGIO (FORÇA DO INSTRUMENTO)         ")
print("================================================================================")
print(iv_res.first_stage)

# 4. O Teste de Sobrevivência: Teste de Wald Acumulado
# O linearmodels IV2SLS tem o método wald_test.
wald_formula = 'Impacto_tech_setor + Impacto_tech_setor_lag1 + Impacto_tech_setor_lag2 + Impacto_tech_setor_lag3 + Impacto_tech_setor_lag4 = 0'

try:
    wald_test = iv_res.wald_test(formula=wald_formula)
    print("\n================================================================================")
    print("               TESTE DE WALD CAUSAL (EFEITO LÍQUIDO EM 1 ANO)                   ")
    print("================================================================================")
    print("Hipótese Nula (H0): O efeito causal acumulado é zero.")
    print(f"Estatística F: {wald_test.stat:.4f}")
    print(f"p-valor:       {wald_test.pval:.4f}")

    if wald_test.pval < 0.05:
        print("\nConclusão: Rejeitamos H0. O impacto causal acumulado é estatisticamente diferente de zero!")
    else:
        print("\nConclusão: Não rejeitamos H0. O impacto causal líquido é nulo.")
except Exception as e:
    print(f"\nAviso: Não foi possível calcular o teste de Wald acumulado ({e})")
