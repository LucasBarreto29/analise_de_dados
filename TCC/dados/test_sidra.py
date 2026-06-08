import requests

url = "https://servicodados.ibge.gov.br/api/v3/agregados?busca=grupamento"
resp = requests.get(url)
for r in resp.json():
    for agg in r['agregados']:
        if 'PNAD Cont' in r['nome'] or 'PNAD Cont' in agg['nome']:
             print(f"Table {agg['id']}: {agg['nome']}")
