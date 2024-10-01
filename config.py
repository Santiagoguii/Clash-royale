from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
class Config:
    # String de conexão com o MongoDB
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')


MONGO_URI= "mongodb+srv://userclash:gmm2509@clashroyale.zisnx.mongodb.net/?retryWrites=true&w=majority&appName=ClashRoyale"
DATABASE_NAME= "mydatabase"

