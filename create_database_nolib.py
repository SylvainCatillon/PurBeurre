import requests as req
import mysql.connector
import config
import pdb

products = {}
nb_pages = 1000//20
#categories_tag = ["cereales-pour-petit-dejeuner", "Biscuits apéritifs", "chips"]
categories_name = ["Céréales pour petit-déjeuner", "Biscuits apéritifs", "Chips", "Biscuits", "Pâtes à tartiner"]
product_keys = ["product_name", "categories", "url", "nutrition_grade_fr", "purchase_places"]
tables_list = [
"Category (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20))",
"Product (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50),\
 category_id SMALLINT UNSIGNED, nutriscore CHAR(1), description TEXT, shop VARCHAR(50),\
 url VARCHAR(100), CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id))",
 "Favory (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, product_id SMALLINT UNSIGNED,\
  CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id))"]

def fill_dict():
	for category in categories_name:
		l = []
		for i in range(nb_pages):
			r = req.get("https://fr.openfoodfacts.org/categorie/{}/{}.json".format(category, str(i+1)))
			result = r.json()
			"""l2 = []
			prod_d = {}
			for e in result["products"]:
				for f in product_keys:
					if f in e.keys():
						prod_d[f] = e[f]
					else:
						prod_d[f] = None
				l2.append({})
			l += l2"""
			l += result["products"]
		products[category] = l

"""def create_db(cursor):
	cursor.execute("CREATE DATABASE pur_beurre DEFAULT CHARACTER SET 'utf8'")"""

def create_tables(cursor):
	for table in tables_list:
		request = "CREATE TABLE IF NOT EXISTS " + table + " ENGINE=INNODB"
		print(request)
		cursor.execute(request)

def fill_tables(products_dict, cursor):
	pass
	"""cursor.execute("CREATE TABLE products (id SMALLINT UNSIGNED AUTO INCREMENT PRIMARY KEY, nom VARCHAR, category_id)")
	sql = "INSERT INTO products (nom, category_id) VALUES (%s,%s)"
	for product in products_dict:
		cursor.execute(sql, (product["product_name"])), #product[category_id]))"""

def fill_db(products_dict):
	cnx = mysql.connector.connect(user= config.user, password = config.password, database = config.database, host = config.host)
	cursor = cnx.cursor()
	cursor.execute("USE pur_beurre")
	try:
		create_tables(cursor)
		fill_tables(products_dict, cursor)
	finally:
		cursor.close()
		cnx.close()

if __name__ == '__main__':
	fill_dict()
	print(len(products["jus-d-orange"]))

