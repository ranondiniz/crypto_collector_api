import requests
from sqlalchemy import create_engine, Column, String, DECIMAL, Integer, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
import os
import time

# Load .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
API_URL = "https://rest.coincap.io/v3/assets?limit=10"
API_KEY = os.getenv("API_KEY")

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Models do Banco
class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'
    id = Column(String(50), primary_key=True)
    rank = Column(Integer, nullable=False)
    symbol = Column(String(10), nullable=False)
    name = Column(String(50), nullable=False)
    supply = Column(DECIMAL(20, 8))
    max_supply = Column(DECIMAL(20, 8))
    prices = relationship("CryptoPrice", back_populates="cryptocurrency")

class CryptoPrice(Base):
    __tablename__ = 'crypto_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cryptocurrency_id = Column(String(50), ForeignKey('cryptocurrencies.id'), nullable=False)
    price_usd = Column(DECIMAL(30, 10), nullable=False)
    volume_usd_24hr = Column(DECIMAL(30, 10))
    market_cap_usd = Column(DECIMAL(30, 10))
    change_percent_24hr = Column(DECIMAL(10, 4))
    vwap_24hr = Column(DECIMAL(30, 10))
    timestamp = Column(BigInteger, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    cryptocurrency = relationship("Cryptocurrency", back_populates="prices")

# Criar tabelas
Base.metadata.create_all(engine)

# Extrair dados
def extrair_dados_coincap():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Tratar dados
def tratar_dados(cripto):
    crypto_model = Cryptocurrency(
        id=cripto['id'],
        rank=int(cripto['rank']),
        symbol=cripto['symbol'],
        name=cripto['name'],
        supply=cripto.get('supply'),
        max_supply=cripto.get('maxSupply')
    )

    price_model = CryptoPrice(
        cryptocurrency_id=cripto['id'],
        price_usd=cripto['priceUsd'],
        volume_usd_24hr=cripto.get('volumeUsd24Hr'),
        market_cap_usd=cripto.get('marketCapUsd'),
        change_percent_24hr=cripto.get('changePercent24Hr'),
        vwap_24hr=cripto.get('vwap24Hr'),
        timestamp=int(datetime.utcnow().timestamp() * 1000)
    )

    return crypto_model, price_model

# Salvar dados
def salvar_no_banco(crypto, price):
    with Session() as session:
        session.merge(crypto)  # Atualiza ou insere
        session.add(price)     # Insere histórico
        session.commit()
        print(f" Salvo: {crypto.name} - {price.price_usd} USD")

# Execução
if __name__ == "__main__":
    while True:
        try:
            print(" Coletando dados da CoinCap...")
            dados = extrair_dados_coincap()
            for cripto in dados:
                crypto, price = tratar_dados(cripto)
                salvar_no_banco(crypto, price)
            print(" Coleta finalizada. Aguardando 15 segundos...\n")
            time.sleep(15)
        except Exception as e:
            print(f" Erro: {e}")
            time.sleep(15)
