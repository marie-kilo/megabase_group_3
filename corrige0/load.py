"""Load: Créer le schéma et écrire dans les tables SQL."""

import os
import pathlib

import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=megabase0")
SCHEMA = pathlib.Path(__file__).resolve().parent / "schema.sql"


def connect():
    return psycopg2.connect(DB_URL)


def create_schema(cur):
    cur.execute(SCHEMA.read_text())


def count_rows(cur, table):
    """Rows already in the table, used to resume where a previous run stopped."""
    cur.execute(f"SELECT count(*) FROM {table}")
    return cur.fetchone()[0]


def insert_communes(cur, communes):
    """Insert the communes and return the set of known INSEE codes."""
    rows = [(c["code"], c["nom"], c.get("population")) for c in communes]
    cur.executemany(
        "INSERT INTO commune (insee_code, name, population) "
        "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        rows,
    )
    return {c["code"] for c in communes}


def insert_chunk(cur, table, key_column, chunk):
    """Insert one chunk of (key, name, insee_code) tuples."""
    cur.executemany(
        f"INSERT INTO {table} ({key_column}, name, insee_code) "
        f"VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        chunk,
    )
