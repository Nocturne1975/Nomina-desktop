import psycopg2
from psycopg2 import sql, OperationalError
import bcrypt

# --- CONFIGURATION DE LA BASE DE DONNÉES ---
DB_HOST = 'ep-royal-dew-ad4wqma8-pooler.c-2.us-east-1.aws.neon.tech'
DB_NAME = 'neondb'
DB_USER = 'neondb_owner'
DB_PASSWORD = 'npg_ilexA4aRfJu0'
SSLMODE = 'require'


def get_connection():
    """Créer une connexion à la base de données via psycopg2."""
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=SSLMODE
    )

# --- UTILITAIRE POUR LES TRANSACTIONS SIMPLES ---
def execute_query(query, params=None, fetch=False):
    """
    Exécuter une requête SQL avec des paramètres facultatifs.
    :param query: La requête SQL (str).
    :param params: Les paramètres pour la requête (%s placeholders).
    :param fetch: Si True, retourne les résultats (requêtes SELECT).
    :return: Résultats (si fetch=True), sinon None.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:  # Retourner les résultats pour les requêtes SELECT
                    return cur.fetchall()
    except OperationalError as e:
        print(f"Erreur de connexion à la base de données : {e}")
    except psycopg2.Error as e:
        print(f"Erreur SQL : {e}")
    return None


# --- CRUD POUR LES CATEGORIES ---
def get_all_categories():
    """Charger toutes les catégories de la table 'Categorie'."""
    query = 'SELECT id, name, description FROM "Categorie"'
    return execute_query(query, fetch=True)


def insert_categorie(name, description):
    """Insérer une nouvelle catégorie dans la table."""
    query = 'INSERT INTO "Categorie" (name, description) VALUES (%s, %s)'
    execute_query(query, params=(name, description))


def update_categorie(id, name, description):
    """Mettre à jour une catégorie existante."""
    query = 'UPDATE "Categorie" SET name=%s, description=%s WHERE id=%s'
    execute_query(query, params=(name, description, id))


def delete_categorie(id):
    """Supprimer une catégorie par son ID."""
    query = 'DELETE FROM "Categorie" WHERE id=%s'
    execute_query(query, params=(id,))


# --- CRUD POUR USERS ---
def get_all_users():
    """Récupérer tous les utilisateurs."""
    query = 'SELECT id, username, email, role, "isActive", "createdAt", "updatedAt" FROM "User"'
    return execute_query(query, fetch=True)


def insert_user(username, password, email, role="Editor", is_active=True):
    """Ajouter un nouvel utilisateur."""
    query = '''
        INSERT INTO "User" (username, password, email, role, "isActive")
        VALUES (%s, %s, %s, %s, %s)
    '''
    execute_query(query, params=(username, password, email, role, is_active))


def update_user(id, username=None, password=None, email=None, role=None, is_active=None):
    """Mettre à jour un utilisateur existant en fonction des champs fournis."""
    fields = []
    values = []
    if username is not None:
        fields.append("username=%s")
        values.append(username)
    if password is not None:
        fields.append("password=%s")
        values.append(password)
    if email is not None:
        fields.append("email=%s")
        values.append(email)
    if role is not None:
        fields.append("role=%s")
        values.append(role)
    if is_active is not None:
        fields.append('"isActive"=%s')
        values.append(is_active)

    if fields:  # Mise à jour uniquement si des champs sont présents
        query = f'UPDATE "User" SET {", ".join(fields)} WHERE id=%s'
        values.append(id)
        execute_query(query, params=tuple(values))


def delete_user(id):
    """Supprimer un utilisateur par son ID."""
    query = 'DELETE FROM "User" WHERE id=%s'
    execute_query(query, params=(id,))


# --- FONCTIONS POUR TITRE ---
def get_all_titres():
    """Récupérer tous les titres et leurs relations (Culture, Categorie)."""
    query = '''
        SELECT T.id, T.valeur, T.type, T.genre, T."cultureId", CU.name, T."categorieId", CA.name,
               T."createdAt", T."updatedAt"
        FROM "Titre" T
        LEFT JOIN "Culture" CU ON T."cultureId" = CU.id
        LEFT JOIN "Categorie" CA ON T."categorieId" = CA.id
    '''
    return execute_query(query, fetch=True)


def insert_titre(valeur, type_field, genre, culture_id, categorie_id):
    """Ajouter un nouveau titre."""
    query = '''
        INSERT INTO "Titre" (valeur, type, genre, "cultureId", "categorieId")
        VALUES (%s, %s, %s, %s, %s)
    '''
    execute_query(query, params=(valeur, type_field, genre, culture_id, categorie_id))


def update_titre(id, valeur, type_field, genre, culture_id, categorie_id):
    """Mettre à jour un titre existant."""
    query = '''
        UPDATE "Titre"
        SET valeur=%s, type=%s, genre=%s, "cultureId"=%s, "categorieId"=%s
        WHERE id=%s
    '''
    execute_query(query, params=(valeur, type_field, genre, culture_id, categorie_id, id))


def delete_titre(id):
    """Supprimer un titre par son ID."""
    query = 'DELETE FROM "Titre" WHERE id=%s'
    execute_query(query, params=(id,))

# --- CRUD POUR CONCEPT ---

def get_all_concepts():
    """
    Récupérer tous les concepts et leurs relations avec les catégories.
    """
    query = '''
        SELECT C.id, C.valeur, C.type, C.mood, C.keywords, C."categorieId", CA.name, 
               C."createdAt", C."updatedAt"
        FROM "Concept" C
        LEFT JOIN "Categorie" CA ON C."categorieId" = CA.id
    '''
    return execute_query(query, fetch=True)


def insert_concept(valeur, type_field, mood, keywords, categorie_id):
    """
    Ajouter un nouveau concept.
    """
    query = '''
        INSERT INTO "Concept" (valeur, type, mood, keywords, "categorieId")
        VALUES (%s, %s, %s, %s, %s)
    '''
    execute_query(query, params=(valeur, type_field, mood, keywords, categorie_id))


def update_concept(id, valeur, type_field, mood, keywords, categorie_id):
    """
    Mettre à jour un concept existant.
    """
    query = '''
        UPDATE "Concept"
        SET valeur=%s, type=%s, mood=%s, keywords=%s, "categorieId"=%s
        WHERE id=%s
    '''
    execute_query(query, params=(valeur, type_field, mood, keywords, categorie_id, id))


def delete_concept(id):
    """
    Supprimer un concept par son ID.
    """
    query = 'DELETE FROM "Concept" WHERE id=%s'
    execute_query(query, params=(id,))

# --- CRUD POUR FRAGMENTSHISTOIRE ---

def get_all_fragments():
    """
    Récupérer tous les fragments d'histoire et leurs relations avec Culture et Categorie.
    """
    query = '''
        SELECT F.id, F.texte, F."appliesTo", F.genre, F."minNameLength", F."maxNameLength",
               F."cultureId", CU.name, F."categorieId", CA.name,
               F."createdAt", F."updatedAt"
        FROM "FragmentsHistoire" F
        LEFT JOIN "Culture" CU ON F."cultureId" = CU.id
        LEFT JOIN "Categorie" CA ON F."categorieId" = CA.id
    '''
    return execute_query(query, fetch=True)


def insert_fragment(texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id):
    """
    Ajouter un nouveau fragment d'histoire.
    """
    query = '''
        INSERT INTO "FragmentsHistoire" (texte, "appliesTo", genre, "minNameLength", "maxNameLength", "cultureId", "categorieId")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    execute_query(query, params=(texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id))


def update_fragment(id, texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id):
    """
    Mettre à jour un fragment d'histoire existant.
    """
    query = '''
        UPDATE "FragmentsHistoire"
        SET texte=%s, "appliesTo"=%s, genre=%s, "minNameLength"=%s, "maxNameLength"=%s, 
            "cultureId"=%s, "categorieId"=%s
        WHERE id=%s
    '''
    execute_query(query, params=(texte, applies_to, genre, min_name_length, max_name_length, culture_id, categorie_id, id))


def delete_fragment(id):
    """
    Supprimer un fragment d'histoire par son ID.
    """
    query = 'DELETE FROM "FragmentsHistoire" WHERE id=%s'
    execute_query(query, params=(id,))
    
# --- CRUD POUR LIEUX ---

def get_all_lieux():
    """
    Récupérer tous les lieux et leurs relations avec les catégories.
    """
    query = '''
        SELECT L.id, L.value, L.type, L."categorieId", C.name, L."createdAt", L."updatedAt"
        FROM "Lieux" L
        LEFT JOIN "Categorie" C ON L."categorieId" = C.id
    '''
    return execute_query(query, fetch=True)


def insert_lieu(value, type_field, categorie_id):
    """
    Ajouter un nouveau lieu.
    """
    query = '''
        INSERT INTO "Lieux" (value, type, "categorieId")
        VALUES (%s, %s, %s)
    '''
    execute_query(query, params=(value, type_field, categorie_id))


def update_lieu(id, value, type_field, categorie_id):
    """
    Mettre à jour un lieu existant.
    """
    query = '''
        UPDATE "Lieux"
        SET value=%s, type=%s, "categorieId"=%s
        WHERE id=%s
    '''
    execute_query(query, params=(value, type_field, categorie_id, id))


def delete_lieu(id):
    """
    Supprimer un lieu par son ID.
    """
    query = 'DELETE FROM "Lieux" WHERE id=%s'
    execute_query(query, params=(id,))
    
# --- CRUD POUR CULTURE ---

def get_all_cultures():
    """
    Récupérer toutes les cultures.
    """
    query = '''
        SELECT id, name, description, "createdAt", "updatedAt"
        FROM "Culture"
    '''
    return execute_query(query, fetch=True)


def insert_culture(name, description):
    """
    Ajouter une nouvelle culture.
    """
    query = '''
        INSERT INTO "Culture" (name, description)
        VALUES (%s, %s)
    '''
    execute_query(query, params=(name, description))


def update_culture(id, name, description):
    """
    Mettre à jour une culture existante.
    """
    query = '''
        UPDATE "Culture"
        SET name=%s, description=%s
        WHERE id=%s
    '''
    execute_query(query, params=(name, description, id))


def delete_culture(id):
    """
    Supprimer une culture par son ID.
    """
    query = 'DELETE FROM "Culture" WHERE id=%s'
    execute_query(query, params=(id,))
    
# --- CRUD POUR NOMPERSONNAGE ---

def get_all_noms_personnages():
    """
    Récupérer tous les noms de personnages et leurs relations avec Categorie.
    """
    query = '''
        SELECT NP.id, NP.valeur, NP."categorieId", CA.name, NP."createdAt", NP."updatedAt"
        FROM "NomPersonnage" NP
        LEFT JOIN "Categorie" CA ON NP."categorieId" = CA.id
    '''
    return execute_query(query, fetch=True)


def insert_nom_personnage(nom, categorie_id):
    """
    Ajouter un nouveau nom de personnage (version simple, sans genre ni culture).
    """
    query = '''
        INSERT INTO "NomPersonnage" (valeur, "categorieId")
        VALUES (%s, %s)
    '''
    execute_query(query, params=(nom, categorie_id))


def update_nom_personnage(id, nom, categorie_id):
    """
    Mettre à jour un nom de personnage existant (version simple, sans genre ni culture).
    """
    query = '''
        UPDATE "NomPersonnage"
        SET valeur=%s, "categorieId"=%s
        WHERE id=%s
    '''
    execute_query(query, params=(nom, categorie_id, id))


def delete_nom_personnage(id):
    """
    Supprimer un nom de personnage par son ID.
    """
    query = 'DELETE FROM "NomPersonnage" WHERE id=%s'
    execute_query(query, params=(id,))
    

    
# --- AUTHENTIFICATION UTILISATEUR ---
import bcrypt

def check_user_credentials(username, password):
    """
    Vérifie l'identifiant et le mot de passe. Le mot de passe est comparé en utilisant bcrypt.
    """
    query = 'SELECT id, username, password, email, role FROM "User" WHERE username=%s'
    result = execute_query(query, params=(username,), fetch=True)
    try:
        if result and bcrypt.checkpw(password.encode(), result[0][2].encode()):
            return result[0]
    except ValueError:
        pass
    return None
