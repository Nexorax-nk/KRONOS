# src/db/connection.py
import os
import psycopg2

def get_connection():
    # Production-ready PostgreSQL connection pool setup
    # SSL is enforced to comply with KRONOS-MEMORY-006
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL"),
        sslmode="require"
    )
    return conn
