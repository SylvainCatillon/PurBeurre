import mysql.connector
from Menu import Menu
from config import connection_config

class ConnectMenu:

	def __init__(self):
		self.cnx = mysql.connector.connect(**connection_config)
		self.cursor = self.cnx.cursor(dictionary=True)

	def __enter__(self):
		return Menu(self.cnx, self.cursor)

	def __exit__(self, type, value, traceback):
		closed = self.cursor.close()
		self.cnx.close()
