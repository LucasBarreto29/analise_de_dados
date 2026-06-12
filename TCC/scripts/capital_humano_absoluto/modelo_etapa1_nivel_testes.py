import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print(" ETAPA 1: MODELO EM NÍVEL E TESTES DE RAIZ UNITÁRIA NAS SÉRIES ORIGINAIS ")
print("="*80)

# 1. Preparação
df = pd.read_csv('/Users/lucas/Desktop/analise_dados/analise_de_dados/TCC/dados/painel_capital_humano_completo.csv')
df['Capital_Humano_FGV'] = pd.to_numeric(df['Capital_Humano_FGV'], errors='coerce')

df['Period'] = pd.PeriodIndex(df['Trimestre'].str.replace('q', 'Q', case=False), freq='Q').to_timestamp()
df = df.set_index(['Setor', 'Period']).sort_index()

# Transformações em Log (Nível)
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df['ln_Capital_FGV'] = np.log(df['Capital_Humano_FGV'])
df['ln_Estoque_TI'] = np.log(df['Estoque_TI_Setor'])
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.dropna(subset=['ln_Produtividade', 'ln_Estoque_TI', 'ln_Capital_FGV', 'Selic'])

# Adicionar defasagens do Estoque TI para o modelo em nível
df['ln_Estoque_TI_lag1'] = df.groupby(level='Setor')['ln_Estoque_TI'].shift(1)
df['ln_Estoque_TI_lag2'] = df.groupby(level='Setor')['ln_Estoque_TI'].shift(2)
df['const'] = 1

df_model = df[['ln_Produtividade', 'ln_Estoque_TI', 'ln_Estoque_TI_lag1', 'ln_Estoque_TI_lag2', 'Selic', 'ln_Capital_FGV', 'const']].dropna()

# 2. Estimação do Modelo em Nível
exog_vars = ['const', 'ln_Estoque_TI', 'ln_Estoque_TI_lag1', 'ln_Estoque_TI_lag2', 'Selic', 'ln_Capital_FGV']
mod = PanelOLS(df_model['ln_Produtividade'], df_model[exog_vars], entity_effects=True)
res = mod.fit(cov_type='unadjusted')

print("\n--- A. RESULTADO DO MODELO EM NÍVEL ---")
print("Observação: Os resultados abaixo podem ser espúrios se as séries forem não-estacionárias (I(1)).")
print(res.summary.tables[1])

# 3. Testes de Raiz Unitária
print("\n--- B. TESTES DE ESTACIONARIEDADE (VARIÁVEIS EM NÍVEL) ---")
print("Iremos testar as variáveis 'ln_Produtividade' e 'ln_Estoque_TI' para cada setor.")

setores = df.index.get_level_values('Setor').unique()
variaveis_teste = ['ln_Produtividade', 'ln_Estoque_TI']

for var in variaveis_teste:
    print(f"\nVariável: {var}")
    print(f"{'Setor':<30} | {'ADF p-val':<12} | {'KPSS p-val':<12} | {'Zivot-Andrews p-val'}")
    print("-" * 80)
    for setor in setores:
        serie = df.xs(setor, level='Setor')[var].dropna()
        if len(serie) < 10:
            continue
            
        # ADF Test (H0: Tem raiz unitária / É não-estacionária)
        try:
            adf_res = adfuller(serie, autolag='AIC')
            adf_p = adf_res[1]
        except:
            adf_p = np.nan
            
        # KPSS Test (H0: É estacionária)
        try:
            kpss_res = kpss(serie, regression='c', nlags='auto')
            kpss_p = kpss_res[1]
        except:
            kpss_p = np.nan
            
        # Zivot-Andrews Test (H0: Tem raiz unitária)
        try:
            za_res = zivot_andrews(serie, regression='c', autolag='AIC')
            za_p = za_res[1]
        except:
            za_p = np.nan
            
        print(f"{setor[:28]:<30} | {adf_p:<12.4f} | {kpss_p:<12.4f} | {za_p:<12.4f}")

print("\nConclusão da Etapa 1:")
print("Se a maioria dos setores apresenta p-valores altos no ADF/ZA (não rejeita raiz unitária)")
print("e p-valores baixos no KPSS (rejeita estacionariedade), isso PROVA que as variáveis em NÍVEL")
print("são integradas de ordem 1 (I(1)). A metodologia exige que elas sejam diferenciadas!")
