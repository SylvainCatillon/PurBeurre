import mysql.connector
from random import choice
from config import database_config as config

class DatabaseSeeker:

	@staticmethod
	def connect():
		return mysql.connector.connect(
			user= config["user"], password = config["password"],
			database = config["database"], host = config["host"])

	def temp_random_product(self):
		cnx = self.connect()
		cursor = cnx.cursor()
		product_id = 0
		category_id = 0
		try:
			cursor.execute("SELECT id FROM Category")
			category_id = choice(cursor.fetchall())[0]
			cursor.execute("SELECT id FROM Product WHERE category_id = %s",
					      (category_id,))
			product_id = choice(cursor.fetchall())[0]
		finally:
			cursor.close()
			cnx.close()
		return product_id, category_id

	def select_substitute(self, cursor, category_id, substitute_score): # static method? dépend du reste du programme
		querry = "SELECT id from Product WHERE category_id = %s and \
		nutriscore = %s"
		cursor.execute(querry, (category_id, substitute_score))
		substitute_id = choice(cursor.fetchall())["id"]
		cursor.execute("SELECT * FROM Product WHERE id = %s", (substitute_id,))
		return cursor.fetchone()


	def find_substitute(self, product_id, category_id):
		sbt_dict = {}
		cnx = self.connect()
		cursor = cnx.cursor(dictionary=True)
		try:
			querry = "SELECT nutriscore FROM Product WHERE category_id = %s \
			and nutriscore < (SELECT nutriscore FROM Product WHERE id = %s) \
			ORDER BY nutriscore LIMIT 1"
			cursor.execute(querry, (category_id, product_id)) # fonction find_nutriscore?
			result = cursor.fetchone()
			if not result:
				print("Il n'y a pas d'alternative plus saine à \
ce produit dans la base de données") # déplacer cette ligne vers Menu.display_substitue?
			else:
				sbt_dict = self.select_substitute(
					cursor, category_id, result["nutriscore"])
		finally:
			cursor.close()
			cnx.close()
		return sbt_dict

	def test_database(self): # a revoir. a utiliser avant et après la création de la db
		cnx = self.connect()
		cursor = cnx.cursor()
		try: # rajouter except?
			categories_name = [name for name in config["categories_name"]]
			cursor.execute("SHOW TABLES")
			tables_list = [tpl[0] for tpl in cursor.fetchall()]
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
				"""for category in config.categories_name:
					cursor.execute("SELECT id FROM Product WHERE category_id = \
						(SELECT id FROM Category WHERE name = %s)", (category,))
					if len(cursor.fetchall()) < config.min_prod_in_db:
						categories_name.append(category)"""
		finally:
			cursor.close()
			cnx.close()
		return categories_name

