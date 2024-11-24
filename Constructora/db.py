import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',          
            user='root',   
            password='',               
            database='constructora',   
            ssl_disabled=True          
        )
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
