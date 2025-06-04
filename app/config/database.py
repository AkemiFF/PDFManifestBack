import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")



def getConnection() :
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e :
        print("Erreur {e}")


def getSessionLocal():
    #DATABASE_URL = "postgresql+psycopg2://postgres.eevnxzwewffagbvdlkgk:WzSu7z8T4KFYpqeL@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    DATABASE_URL = "postgresql+psycopg2://postgres:pass@localhost:5432/manifest"
    engine = create_engine(DATABASE_URL)


    # Création d'une session
    SessionLocal = sessionmaker(bind=engine,autoflush=True)
    session = SessionLocal()
    return session