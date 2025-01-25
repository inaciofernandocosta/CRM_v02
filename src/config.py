import os

# Obter a chave da OpenAI do ambiente
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
