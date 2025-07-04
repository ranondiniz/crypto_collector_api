from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host="dpg-d1jk2bq4d50c738465s0-a.oregon-postgres.render.com",
    port=5432,
    db_name="database_crypto",
    user="database_crypto_user",
    password="Up5zjj9ZuXl5a8Cb9rbJfq5hqMdxthc1",
    table_schema="public",
)

# Create an agent with the PostgresTools
agent = Agent(tools=[postgres_tools],
              model=Groq(id="llama3-70b-8192"),
              description="Você é um engenheiro de dados com acesso a um banco PostgreSQL com tabelas sobre criptomoedas."
)

agent.print_response("Liste todas as tabelas disponíveis no schema public do banco PostgreSQL.", markdown=True)

agent.print_response("Liste os nomes e ids das criptomoedas disponíveis na base.")

agent.print_response("Qual é a criptomoeda com maior valor de mercado atualmente?")