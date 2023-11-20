import mysql.connector


db = mysql.connector.connect(
    host="servinfo-maria",user = "brisset", password = "brisset", database = "DBbrisset"
)

def get_cursor():
    return db.cursor()

def close_cursor(cursor):
    cursor.close()

def execute_query(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

def get_id_utilisateur_max(cursor):
    query = "SELECT MAX(id_utilisateur) FROM UTILISATEUR"
    execute_query(cursor, query)
    return cursor.fetchone()[0]

def liste_billets():
    try:
        cursor = get_cursor()
        query = "SELECT * FROM BILLET"
        execute_query(cursor, query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e.args)
    return None

def les_type_billets():
    try:
        cursor = get_cursor()
        query = "SELECT * FROM BILLET_TYPE"
        execute_query(cursor, query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e.args)
    return None


def liste_utilisateurs():
    try:
        cursor = get_cursor()
        query = "SELECT * FROM UTILISATEUR"
        execute_query(cursor, query)
        result = cursor.fetchall()
        close_cursor(cursor)
        return result
    except Exception as e:
        print(e.args)
    return None

def save_inscription(nom, tel, email, mdp):
    try:
        cursor = get_cursor()
        query = "INSERT INTO UTILISATEUR (id_utilisateur, nom_user, tel, mail, mot_de_passe, id_role) VALUES (%s, %s, %s, %s, %s, %s)"
        id_utilisateur = get_id_utilisateur_max(cursor) + 1
        id_role = 1 # Trouver comment on fait pour le role
        params = (id_utilisateur, nom, tel, email, mdp, id_role)
        execute_query(cursor, query, params)
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def verif_connexion(email, mdp):
    try:
        cursor = get_cursor()
        query = "SELECT * FROM UTILISATEUR WHERE mail = %s AND mot_de_passe = %s"
        params = (email, mdp)
        execute_query(cursor, query, params)
        result = cursor.fetchone()
        close_cursor(cursor)
        return result
    except Exception as e:
        print(e.args)
    return None