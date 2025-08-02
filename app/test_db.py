import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()  # Load variables from .env

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("✅ Connected to the database successfully.")
    conn.close()

except Exception as e:
    print("❌ Failed to connect:", e)
