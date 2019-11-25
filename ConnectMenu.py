import mysql.connector
from menu import Menu
from config import connection_config


class ConnectMenu:
    """Context manager to assure the closing of the database connection
    at the end of the program"""

    def __init__(self):
        self.cnx = mysql.connector.connect(**connection_config)
        self.cursor = self.cnx.cursor(dictionary=True)

    def __enter__(self):
        return Menu(self.cnx, self.cursor)

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.cnx.close()
