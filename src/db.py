import psycopg2
from psycopg2 import sql


DB_HOST = 'ep-royal-dew-ad4wqma8-pooler.c-2.us-east-1.aws.neon.tech'
DB_NAME = 'neondb'
DB_USER = 'neondb_owner'
DB_PASSWORD = 'npg_ilexA4aRfJu0'
SSLMODE = 'require'


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def check_user_credentials(username, password):
    # Pour les tests, on accepte n'importe quel login
    return True


def insert_categorie(name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "Categorie" (name, description) VALUES (%s, %s)', (name, description))
    conn.commit()
    cur.close()
    conn.close()

def update_categorie(id, name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE "Categorie" SET name=%s, description=%s WHERE id=%s', (name, description, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_categorie(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "Categorie" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()