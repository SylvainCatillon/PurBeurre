from random import choice, sample
import config

class DatabaseSeeker:

	def __init__(self, cursor, cnx):
		self.cursor = cursor
		self.cnx = cnx

	def random_products(self, category_id):
		"""Randomly selects products from the given category.
		Change proposed_products in config.py to change the number of
		products proposed to the user"""
		querry = "SELECT name, category_id, nutriscore FROM Product \
		WHERE category_id = %s"
		self.cursor.execute(querry, (category_id,))
		all_products = self.cursor.fetchall()
		products_list = sample(all_products, config.nb_proposed_prod)
		return products_list

	def find_substitute(self, product):
		"""Finds a substitute for a given product (must be a dict 
		with at least 'nustriscore' and 'category_id' as keys)
		-Select the higher nutriscore of the product's category
		-If there is no higher nutriscore, return an empty dict
		-Else, select a random product between the possible subsitutes
		and return a dict with all the informations of this product"""
		sbt_dict = {}
		cursor = self.cursor
		querry = "SELECT nutriscore FROM Product WHERE category_id = %s \
		and nutriscore < %s ORDER BY nutriscore LIMIT 1"
		cursor.execute(
			querry, (product["category_id"], product["nutriscore"]))
		result = self.cursor.fetchone()
		if result:
			querry = "SELECT id from Product WHERE category_id = %s and \
			nutriscore = %s"
			cursor.execute(
				querry, (product["category_id"], result["nutriscore"]))
			substitute_id = choice(cursor.fetchall())["id"]
			cursor.execute(
				"SELECT * FROM Product WHERE id = %s", (substitute_id,))
			sbt_dict = cursor.fetchone()
		return sbt_dict

	def see_categories(self):
		cursor = self.cursor
		cursor.execute("SELECT id, name FROM Category")
		good_categories = []
		low_categories = []
		for category_dict in cursor.fetchall():
			cursor.execute(
				"SELECT id FROM Product WHERE category_id = %s LIMIT %s", (
					category_dict["id"], config.min_prod_in_db))
			products = cursor.fetchall()
			if len(products) >= config.min_prod_in_db:
				good_categories.append(category_dict)
			else:
				low_categories.append(category_dict)
		return good_categories, low_categories

	def save_product(self, product_id):
		"""Save the id of a product into the table Favory"""
		self.cursor.execute(
			"INSERT INTO Favory (product_id) VALUES (%s)", (product_id,))
		self.cnx.commit()

	def is_saved(self, product_id):
		self.cursor.execute(
			"SELECT id FROM Favory WHERE product_id = %s", (product_id,))
		result = self.cursor.fetchall()
		if result:
			return True
		return False

	def see_favories(self):
		"""Returns all the saved substitutes, as a list of dict"""
		cursor = self.cursor
		favories = []
		cursor.execute("SELECT product_id FROM Favory ORDER BY id")
		for dico in cursor.fetchall():
			cursor.execute(
				"SELECT * FROM Product WHERE id = %s", (dico["product_id"],))
			favories.append(cursor.fetchone())
		return favories

	def test_database(self): # a revoir. a utiliser avant et après la création de la db
		cursor = self.cursor
		categories_name = list(config.categories_name) # To create a new list and not change the initial one
		cursor.execute("SHOW TABLES")
		tables_list = [list(dico.values())[0] for dico in cursor.fetchall()]
		if "category" in tables_list and "product" in tables_list:
			cursor.execute("SELECT id, name FROM Category")
			db_categories = cursor.fetchall()
			for category in db_categories:
				if category["name"] in categories_name:
					categories_name.remove(category["name"])
				else:
					cursor.execute("DELETE FROM Category WHERE id = %s",(
						category["id"],))
		return categories_name

	"""def test_database(self): # a revoir. a utiliser avant et après la création de la db
		cursor = self.cursor
		categories_name = list(config.categories_name) # To create a new list and not change the initial one
		cursor.execute("SHOW TABLES")
		tables_list = [list(dico.values())[0] for dico in cursor.fetchall()]
		if "category" in tables_list and "product" in tables_list:
			i = 0
			while i < len(categories_name): # if describe category == les bonne values???
				category = categories_name[i]
				cursor.execute("SELECT id FROM Product WHERE category_id = \
					(SELECT id FROM Category WHERE name = %s)", (category,))
				if  len(cursor.fetchall()) > config.min_prod_in_db:
					categories_name.remove(category)
				else:
					i += 1
		return categories_name"""

