from dotenv import load_dotenv
import os

load_dotenv()


class Environment():
    def __init__(self):
        self.MONGO_URI = os.getenv("MONGO_URI")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = int(os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.TOKEN_TYPE = "bearer"
        self.TOKEN_KEY = "token"
