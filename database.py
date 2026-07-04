# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


# ==========================================================
# DATABASE CONNECTION
# ==========================================================
def get_connection():
    return psycopg2.connect(DATABASE_URL,sslmode="require")

# ==========================================================
# CREATE DATABASE TABLE
# ==========================================================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            token VARCHAR(20),
            name VARCHAR(100),
            age INTEGER,
            gender VARCHAR(20),
            phone VARCHAR(20),
            department VARCHAR(100),
            symptoms TEXT,
            status VARCHAR(30),
            date_time VARCHAR(50)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
