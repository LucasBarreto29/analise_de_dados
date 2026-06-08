import pandas as pd
import numpy as np
import os
import warnings
from statsmodels.tsa.stattools import zivot_andrews

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(os.path.join(BASE_DIR, "dados", "painel_mestre.csv"))
df['ln_Produtividade'] = np.log(df['Produtividade_Hora_Habitual'])
df.sort_values(by=['Setor', 'Trimestre'], inplace=True)
df['d_ln_Produtividade'] = df.groupby('Setor')['ln_Produtividade'].diff()

setores_problematicos = ['Comércio', 'Serviços Imobiliários', 'Transporte']

print("="*70)
print(" DIAGNÓSTICO DE RAIZ UNITÁRIA COM QUEBRA ESTRUTURAL (ZIVOT-ANDREWS) ")
print("="*70)

for setor in setores_problematicos:
    print(f"\n[{setor}]")
    dados_setor = df[df['Setor'] == setor].copy()
    dados_setor = dados_setor.dropna(subset=['d_ln_Produtividade']) # Remove NaNs gerados pela diff
    dados_setor = dados_setor.reset_index(drop=True)
    
    # Teste em Nível
    za_nivel = zivot_andrews(dados_setor['ln_Produtividade'], regression='ct', autolag='AIC', maxlag=4)
    # O user sugeriu res[3], vamos checar se é o 3 ou 4 na versão do statsmodels atual.
    # Geralmente é baselag(3) e bpidx(4).
    idx_quebra_nivel = za_nivel[4] if len(za_nivel) > 4 else za_nivel[3]
    try:
        data_quebra_nivel = dados_setor['Trimestre'].iloc[idx_quebra_nivel]
    except Exception:
        data_quebra_nivel = f"Idx {idx_quebra_nivel} out of bounds"
    
    # Teste em Diferenças
    za_diff = zivot_andrews(dados_setor['d_ln_Produtividade'], regression='ct', autolag='AIC', maxlag=4)
    idx_quebra_diff = za_diff[4] if len(za_diff) > 4 else za_diff[3]
    try:
        data_quebra_diff = dados_setor['Trimestre'].iloc[idx_quebra_diff]
    except Exception:
        data_quebra_diff = f"Idx {idx_quebra_diff} out of bounds"
    
    print(f"  Em Nível:")
    print(f"    P-value: {za_nivel[1]:.4f} | Quebra detectada em: {data_quebra_nivel}")
    print(f"    Conclusão: {'Estacionária (com quebra)' if za_nivel[1] < 0.05 else 'Não-Estacionária'}")
    
    print(f"  Em 1ª Diferença:")
    print(f"    P-value: {za_diff[1]:.4f} | Quebra detectada em: {data_quebra_diff}")
    print(f"    Conclusão: {'Estacionária (com quebra)' if za_diff[1] < 0.05 else 'Não-Estacionária'}")

print("\n" + "="*70)
