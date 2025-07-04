import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY") # Mantenha por boa prática, mas não é estritamente necessário para o endpoint /assets
API_URL = "https://rest.coincap.io/v3/assets?limit=10"
def extrair():
    """
    Faz a requisição para a API CoinCap e retorna os dados JSON.
    """
    url = "https://rest.coincap.io/v3/assets"
    
    # Passando a chave da API como parâmetro, mesmo que opcional para /assets
    params = {"apiKey": API_KEY}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Isso vai levantar um erro para status codes 4xx/5xx
    return response.json()

def transformar(dados_json):
    """
    Processa os dados JSON da API CoinCap, selecionando as 10 principais criptomoedas
    e extraindo informações relevantes para cada uma.
    Retorna uma lista de dicionários com os dados tratados.
    """
    criptos_tratadas = []
    
    # Acessa a lista de ativos dentro da chave 'data'
    data = dados_json.get('data', []) 
    
    criptos_selecionadas = data[:10]
    
    for cripto in criptos_selecionadas:
        # Usamos .get() para evitar KeyErrors se alguma chave estiver faltando
        nome = cripto.get('name', 'N/A')
        simbolo = cripto.get('symbol', 'N/A')
        preco = float(cripto.get('priceUsd', 0.0))
        volume_24h = float(cripto.get('volumeUsd24Hr', 0.0))
        capitalizacao = float(cripto.get('marketCapUsd', 0.0))
        
        dados_tratados = {
            "nome": nome,
            "simbolo": simbolo,
            "preco_usd": round(preco, 2), # Arredonda para 2 casas decimais
            "volume_24h_usd": round(volume_24h, 2),
            "capitalizacao_mercado_usd": round(capitalizacao, 2)
        }
        criptos_tratadas.append(dados_tratados)
        
    return criptos_tratadas

if __name__ == "__main__":
    try:
        dados_json = extrair()
        dados_tratados = transformar(dados_json)
        
        print("Informações das 10 principais criptomoedas (dados tratados):")
        for cripto in dados_tratados:
            print(f"  {cripto['nome']} ({cripto['simbolo']}) - Preço: ${cripto['preco_usd']:.2f}, Volume 24h: ${cripto['volume_24h_usd']:.2f}, Cap. Mercado: ${cripto['capitalizacao_mercado_usd']:.2f}")
            
        # Opcional: Para ver a estrutura completa dos dados tratados
        # print("\nEstrutura JSON dos dados tratados:")
        # print(json.dumps(dados_tratados, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ou obter dados da API: {e}")
    except KeyError as e:
        print(f"Erro ao processar os dados da API: Chave esperada não encontrada - {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")