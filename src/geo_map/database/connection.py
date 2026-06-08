from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
NAME = os.getenv("USERNAME_SUPABASE")
PASSWORD = os.getenv("PASSWORD_SUPABASE")


DATABASE_URL = f"postgresql://{NAME}:{PASSWORD}@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

engine = create_engine(
    DATABASE_URL
)