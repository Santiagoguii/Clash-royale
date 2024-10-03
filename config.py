from dotenv import load_dotenv
import os
from pathlib import Path
from mongoengine import connect

# Carrega variáveis de ambiente do arquivo .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    API_TOKEN = os.getenv('API_TOKEN')

# Conexão com o MongoDB usando o mongoengine
def init_mongo_connection():
    connect(
        db=Config.DATABASE_NAME,  
        host=Config.MONGO_URI,    
        alias='default'           
    )

init_mongo_connection()
