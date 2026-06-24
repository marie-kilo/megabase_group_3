from dotenv import load_dotenv
import psycopg2
from psycopg2 import errors
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME_INIT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

conn.autocommit = True

cur=conn.cursor()

try:
    cur.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
except errors.DuplicateDatabase:
    print("La base existe déjà")

cur.close()
conn.close()


conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cur.execute(sql)

conn.commit()

cur.close()
conn.close()

print("Base créée avec succès")