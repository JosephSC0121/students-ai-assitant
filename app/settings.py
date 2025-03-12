from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os 

load_dotenv()

# DATABASE

DB_USER = os.getenv("DATABASE_USER")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PASSWORD =os.getenv("DATABASE_PASSWORD")
DB_DATABASE =os.getenv("DATABASE_NAME")
DB_PORT = os.getenv("DATABASE_PORT")

# TOKEN SETTINGS
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Encrypt

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


