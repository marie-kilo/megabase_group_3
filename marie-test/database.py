import psycopg2
import os

class Database:
    def __init__(self):
        # Utilise les variables de ton .env
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        
    def execute(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()

    def close(self):
        self.conn.close()