import mysql.connector
from random import choice, sample
from config import database_config as config

class DatabaseSeeker:

	def __init__(self, cursor, cnx):
		self.cursor = cursor
		self.cnx = cnx

	"""@staticmethod
	def connect():
		return mysql.connector.connect(
			user= config["user"], password = config["password"],
			database = config["database"], host = config["host"])"""

	"""def temp_random_product(self):
		cnx = self.connect()
		cursor = cnx.cursor()
		product_id = 0
		category_id = 0
		try:
			cursor.execute("SELECT id FROM Category")
			category_id = choice(cursor.fetchall())["id"]
			cursor.execute("SELECT id FROM Product WHERE category_id = %s",
					      (category_id,))
			product_id = choice(cursor.fetchall())["id"]
		finally:
			cursor.close()
			cnx.close()
		return product_id, category_id"""

	def random_products(self, category_name):
		cursor = self.cursor
		cursor.execute("SELECT id FROM Category WHERE name = %s",
			(category_name,))
		category_id = self.cursor.fetchone()["id"]
		cursor.execute("SELECT id, name FROM Product WHERE category_id=%s",
				      (category_id,))
		all_products = cursor.fetchall() # ou [tpl[0] for tpl in cursor.fetchall()] si je ne veux que le nom
		products_list = sample(all_products, config["proposed_products"])
		return products_list, category_id

	def select_substitute(self, category_id, substitute_score): # static method? dépend du reste du programme
		cursor = self.cursor
		querry = "SELECT id from Product WHERE category_id = %s and \
		nutriscore = %s"
		cursor.execute(querry, (category_id, substitute_score))
		substitute_id = choice(cursor.fetchall())["id"]
		cursor.execute("SELECT * FROM Product WHERE id = %s", (substitute_id,))
		return cursor.fetchone()


	def find_substitute(self, product_id, category_id):
		sbt_dict = {}
		querry = "SELECT nutriscore FROM Product WHERE category_id = %s \
		and nutriscore < (SELECT nutriscore FROM Product WHERE id = %s) \
		ORDER BY nutriscore LIMIT 1"
		self.cursor.execute(querry, (category_id, product_id)) # fonction find_nutriscore?
		result = self.cursor.fetchone()
		if result:
			sbt_dict = self.select_substitute(category_id, result["nutriscore"])
		return sbt_dict

	def save_substitute(self, substitute_id):
		self.cursor.execute("INSERT INTO Favory (product_id) VALUES (%s)",
			(substitute_id,))
		self.cnx.commit()

	def see_favories(self):
		cursor = self.cursor
		favories = []
		cursor.execute("SELECT product_id FROM Favory")
		result = cursor.fetchall() # for e in cursor?
		for dico in result:
			cursor.execute("SELECT * FROM Product WHERE id = %s", (dico["product_id"],))
			favories.append(cursor.fetchone())
		return favories

	def test_database(self): # a revoir. a utiliser avant et après la création de la db
		cursor = self.cursor
		categories_name = list(config["categories_name"]) # To create a new list and not change the initial one
		cursor.execute("SHOW TABLES")
		tables_list = [list(dico.values())[0] for dico in cursor.fetchall()]
		if "category" in tables_list and "product" in tables_list:
			i = 0
			while i < len(categories_name): # if describe category == les bonne values???
				category = categories_name[i]
				cursor.execute("SELECT id FROM Product WHERE category_id = \
					(SELECT id FROM Category WHERE name = %s)", (category,))
				if  len(cursor.fetchall()) > config["min_prod_in_db"]:
					categories_name.remove(category)
				else:
					i += 1
		return categories_name

