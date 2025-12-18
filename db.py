# db.py
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''  # LAISSE VIDE si pas de mot de passe
        self.database = 'universite'
        self.port = 3306

config = DatabaseConfig()

try:
    pool = pooling.MySQLConnectionPool(
        pool_name="app_pool",
        pool_size=5,
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database,
        port=config.port,
        autocommit=False
    )
    print(" Pool de connexions créé")
except Error as e:
    print(f"❌ Erreur: {e}")
    pool = None

def get_connection():
    if pool is None:
        raise Exception("Pool non initialisé")
    
    try:
        connection = pool.get_connection()
        return connection
    except Error as e:
        print(f"❌ Erreur: {e}")
        raise

def test_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            print(f" Connecté à MySQL")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"📊 Base: {db_name[0]}")
            cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f" Erreur: {e}")
        return False

if __name__ == "__main__":
    test_connection()