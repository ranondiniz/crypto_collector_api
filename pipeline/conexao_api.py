import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY") 
API_URL = "https://rest.coincap.io/v3/assets?limit=10"

# Passando a chave como parâmetro 
headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    data = response.json()['data']

    # Coleta as informações das 10 primeiras moedas para teste
    criptos_selecionadas = data[:10]

    print("Informações das 10 principais criptomoedas:")
    for cripto in criptos_selecionadas:
        nome = cripto.get('name', 'N/A')
        simbolo = cripto.get('symbol', 'N/A')
        preco = float(cripto.get('priceUsd', 0.0))
        volume_24h = float(cripto.get('volumeUsd24Hr', 0.0))
        capitalizacao = float(cripto.get('marketCapUsd', 0.0))

        print(f"  {nome} ({simbolo}) - Preço: ${preco:.2f}, Volume 24h: ${volume_24h:.2f}, Cap. Mercado: ${capitalizacao:.2f}")

else:
    print("Erro na API:", response.status_code)
    print(response.text)

