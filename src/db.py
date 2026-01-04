# CRUD pour Titre
def get_all_titres():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT T.id, T.valeur, T.type, T.genre, T.cultureId, CU.name, T.categorieId, CA.name, T.createdAt, T.updatedAt
        FROM "Titre" T
        LEFT JOIN "Culture" CU ON T.cultureId = CU.id
        LEFT JOIN "Categorie" CA ON T.categorieId = CA.id
    ''')
    titres = cur.fetchall()
    cur.close()
    conn.close()
    return titres

def insert_titre(valeur, type_field, genre, culture_id, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO "Titre" (valeur, type, genre, cultureId, categorieId)
        VALUES (%s, %s, %s, %s, %s)
    ''', (valeur, type_field, genre, culture_id, categorie_id))
    conn.commit()
    cur.close()
    conn.close()

def update_titre(id, valeur, type_field, genre, culture_id, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE "Titre"
        SET valeur=%s, type=%s, genre=%s, cultureId=%s, categorieId=%s
        WHERE id=%s
    ''', (valeur, type_field, genre, culture_id, categorie_id, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_titre(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "Titre" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

# CRUD pour Concept
def get_all_concepts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT C.id, C.valeur, C.type, C.mood, C.keywords, C.categorieId, CA.name, C.createdAt, C.updatedAt
        FROM "Concept" C
        LEFT JOIN "Categorie" CA ON C.categorieId = CA.id
    ''')
    concepts = cur.fetchall()
    cur.close()
    conn.close()
    return concepts

def insert_concept(valeur, type_field, mood, keywords, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO "Concept" (valeur, type, mood, keywords, categorieId)
        VALUES (%s, %s, %s, %s, %s)
    ''', (valeur, type_field, mood, keywords, categorie_id))
    conn.commit()
    cur.close()
    conn.close()

def update_concept(id, valeur, type_field, mood, keywords, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE "Concept"
        SET valeur=%s, type=%s, mood=%s, keywords=%s, categorieId=%s
        WHERE id=%s
    ''', (valeur, type_field, mood, keywords, categorie_id, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_concept(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "Concept" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()
# CRUD pour FragmentsHistoire
def get_all_fragments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT F.id, F.texte, F.appliesTo, F.genre, F.minNameLength, F.maxNameLength,
               F.cultureId, CU.name, F.categorieId, CA.name
        FROM "FragmentsHistoire" F
        LEFT JOIN "Culture" CU ON F.cultureId = CU.id
        LEFT JOIN "Categorie" CA ON F.categorieId = CA.id
    ''')
    fragments = cur.fetchall()
    cur.close()
    conn.close()
    return fragments

def insert_fragment(texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO "FragmentsHistoire" (texte, appliesTo, genre, minNameLength, maxNameLength, cultureId, categorieId)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id))
    conn.commit()
    cur.close()
    conn.close()

def update_fragment(id, texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE "FragmentsHistoire"
        SET texte=%s, appliesTo=%s, genre=%s, minNameLength=%s, maxNameLength=%s, cultureId=%s, categorieId=%s
        WHERE id=%s
    ''', (texte, appliesTo, genre, minNameLength, maxNameLength, culture_id, categorie_id, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_fragment(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "FragmentsHistoire" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()
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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM "User" WHERE username=%s AND password=%s', (username, password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

# CRUD pour Categorie
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

# Nouvelle fonction pour lire toutes les catégories
def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description FROM "Categorie"')
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return categories

# Nouvelle fonction pour lire tous les utilisateurs
def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email, role, isActive, createdAt, updatedAt FROM "User"')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

# CRUD pour User
def insert_user(username, password, email, role="Editor", isActive=True):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "User" (username, password, email, role, isActive) VALUES (%s, %s, %s, %s, %s)', (username, password, email, role, isActive))
    conn.commit()
    cur.close()
    conn.close()

def update_user(id, username=None, password=None, email=None, role=None, isActive=None):
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    if username is not None:
        fields.append('username=%s')
        values.append(username)
    if password is not None:
        fields.append('password=%s')
        values.append(password)
    if email is not None:
        fields.append('email=%s')
        values.append(email)
    if role is not None:
        fields.append('role=%s')
        values.append(role)
    if isActive is not None:
        fields.append('isActive=%s')
        values.append(isActive)
    if fields:
        query = f'UPDATE "User" SET {", ".join(fields)} WHERE id=%s'
        values.append(id)
        cur.execute(query, tuple(values))
        conn.commit()
    cur.close()
    conn.close()

def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "User" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    

# CRUD pour Culture
def get_all_cultures():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description FROM "Culture"')
    cultures = cur.fetchall()
    cur.close()
    conn.close()
    return cultures

def insert_culture(name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "Culture" (name, description) VALUES (%s, %s)', (name, description))
    conn.commit()
    cur.close()
    conn.close()

def update_culture(id, name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE "Culture" SET name=%s, description=%s WHERE id=%s', (name, description, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_culture(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "Culture" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

# CRUD NomPersonnage
def get_all_nom_personnages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nom, prenom, categorie_id, culture_id FROM "NomPersonnage"')
    noms = cur.fetchall()
    cur.close()
    conn.close()
    return noms

def insert_nom_personnage(nom, prenom, categorie_id, culture_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "NomPersonnage" (nom, prenom, categorie_id, culture_id) VALUES (%s, %s, %s, %s)', (nom, prenom, categorie_id, culture_id))
    conn.commit()
    cur.close()
    conn.close()

def update_nom_personnage(id, nom, prenom, categorie_id, culture_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE "NomPersonnage" SET nom=%s, prenom=%s, categorie_id=%s, culture_id=%s WHERE id=%s', (nom, prenom, categorie_id, culture_id, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_nom_personnage(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "NomPersonnage" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

# CRUD pour Lieux
def get_all_lieux():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT L.id, L.value, L.type, L.categorieId, C.name
        FROM "Lieux" L
        LEFT JOIN "Categorie" C ON L.categorieId = C.id
    ''')
    lieux = cur.fetchall()
    cur.close()
    conn.close()
    return lieux

def insert_lieu(value, type_field, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "Lieux" (value, type, categorieId) VALUES (%s, %s, %s)', (value, type_field, categorie_id))
    conn.commit()
    cur.close()
    conn.close()

def update_lieu(id, value, type_field, categorie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE "Lieux" SET value=%s, type=%s, categorieId=%s WHERE id=%s', (value, type_field, categorie_id, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_lieu(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM "Lieux" WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

