#  Crypto Data Pipeline

&#x20;&#x20;

Um projeto de engenharia de dados completo e funcional para **coleta automatizada de cotações de criptomoedas**, com persistência em banco **PostgreSQL** via Cloud com **Render**, visualização em **Power BI** e análise via **Agno AI Agent**.

---

##  Estrutura do Projeto

```
Crypto_Collector-API/
├── pipeline/
│   ├── conexao_api.py
│   ├── conexao_tratamento.py
│   ├── database_tratamento.py
├── agents/
│   ├── main_agent1.py
│   └── main_agent2.py
├── dashboards/
│   └── crypto_collector_api.pbix
└── .env
└── .gitignore
└── README.md
└── requirements.txt

```

---

##  Funcionalidades

-  Coleta periódica de dados da [API CoinCap](https://docs.coincap.io/)
-  Armazenamento em banco PostgreSQL (com histórico de preços)
-  Dashboard Power BI com análise das cotações
-  Agente AI (usando `agno` + `groq`) para consulta em linguagem natural ao banco

---

##  Requisitos

- Python 3.11+
- PostgreSQL (local ou em nuvem)
- Conta na [CoinCap](https://coincap.io/)
- Conta no [Groq](https://console.groq.com/) e chave API
- Power BI Desktop (opcional para visualização)

---

##  Instalação

```bash
# Clone o repositório
git clone https://github.com//crypto-collector-api.git
cd crypto-collector-api

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

##  Configuração (.env)

Crie um arquivo `.env` na raiz com as seguintes variáveis:

```
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
API_KEY=chave_da_api_coincap
GROQ_API_KEY=chave_da_api_groq
```

---

##  Como executar

### Executar o coletor de dados:

```bash
cd pipeline
python database_tratamento.py
```

### Executar o agente para consultas:

```bash
cd agents
python main_agent2.py
```

---

##  Dashboard Power BI

Abra o arquivo `crypto_collector_api.pbix` na pasta `dashboard/` e atualize a fonte de dados com sua conexão PostgreSQL.

---

##  Exemplos de perguntas para o Agno:

- `Quais são as criptomoedas disponíveis no banco?`
- `Qual foi o preço mais recente do Bitcoin?`
- `Analise a evolução do preço do Ethereum nos últimos dias.`
- `Mostre o volume de mercado das top 5 criptos.`

---

##  Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais detalhes.

---

##  Agradecimentos

- [CoinCap API](https://docs.coincap.io/)
- [Groq](https://console.groq.com/)
- [Agno AI](https://pypi.org/project/agno/)
- [Render](https://render.com/) para hospedagem PostgreSQL gratuita

