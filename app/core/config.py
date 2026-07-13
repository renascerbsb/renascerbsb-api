import os

from dotenv import load_dotenv

load_dotenv()

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "troque-esta-chave-em-producao")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
