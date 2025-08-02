import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # <-- This line is essential

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),  # Must be loaded from .env
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
