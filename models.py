import mysql.connector


db = mysql.connector.connect(
    host="servinfo-maria",user = "sevellec", password = "sevellec", database = "DBsevellec"
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
