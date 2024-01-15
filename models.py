import mysql.connector

db = mysql.connector.connect(
    host="servinfo-maria",user = "ozocak", password = "ozocak", database = "DBozocak"
)

compte = None

def get_cursor():
    return db.cursor()

def close_cursor(cursor):
    cursor.close()

def execute_query(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

def verif_connexion(pseudo, mdp):
    cursor = get_cursor()
    query = "SELECT * FROM UTILISATEUR WHERE PSEUDO = %s AND MOT_DE_PASSE = %s;"
    cursor.execute(query, (pseudo, mdp))
    utilisateur = cursor.fetchone()
    close_cursor(cursor)
    if utilisateur is not None:
        setup_compte(pseudo)
    return utilisateur

def save_inscription(pseudo, mdp):
    cursor = get_cursor()
    query = "INSERT INTO UTILISATEUR (PSEUDO, MOT_DE_PASSE) VALUES (%s, %s);"
    cursor.execute(query, (pseudo, mdp))
    db.commit()
    close_cursor(cursor)
    setup_compte(pseudo)
    
def setup_compte(pseudo):
    global compte
    cursor = get_cursor()
    query = "SELECT * FROM UTILISATEUR WHERE PSEUDO = %s;"
    cursor.execute(query, (pseudo,))
    user = cursor.fetchone()
    close_cursor(cursor)
    compte = (user[0],user[-1])

def nouveau_festival():
    cursor = get_cursor()
    query = "INSERT INTO FESTIVAL (NOM) VALUES ('Nouveau festival');"
    cursor.execute(query)
    db.commit()
    close_cursor(cursor)
    
def get_festival():
    cursor = get_cursor()
    query = "SELECT * FROM FESTIVAL;"
    cursor.execute(query)
    festival = cursor.fetchall()
    close_cursor(cursor)
    return festival
    
def get_compte():
    global compte
    return compte

def deconnexion():
    global compte
    compte = None