import mysql.connector
from config import database_config as config

class DatabaseHandler:

	
	PRODUCT_TAGS = ["product_name", "brands", "generic_name_fr", "url",
					"nutrition_grade_fr", "stores"]
	TABLES_LIST = [
		"Category (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
 name VARCHAR(50) UNIQUE)",
		"Product (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, \
name VARCHAR(50) UNIQUE, category_id SMALLINT UNSIGNED, \
nutriscore CHAR(1), description TEXT, shop VARCHAR(50), \
url VARCHAR(100), INDEX ind_cat_nutri (category_id, nutriscore), \
CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id))",
		"Favory (id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, \
product_id SMALLINT UNSIGNED, CONSTRAINT fk_product_id FOREIGN KEY \
(product_id) REFERENCES Product(id))"
]

	def __init__(self, products_dict):
		self.products_dict = products_dict
		print("DatabaseHandler created")


	@staticmethod
	def connect():
		return mysql.connector.connect(
			user= config["user"], password = config["password"],
			database = config["database"], host = config["host"])

	def create_tables(self, cursor):
		for table in self.TABLES_LIST:
			request = "CREATE TABLE IF NOT EXISTS " + table + " ENGINE=INNODB"
			cursor.execute(request)

	def verify_product(self, product):
		for tag in self.PRODUCT_TAGS:
			if tag not in product.keys() or not product[tag]:
				if tag in ("stores", "brands"):
					product[tag] = ""
				else:
					return None
		return product

	def fill_tables(self, cursor):
		for category, products_list in self.products_dict.items():
			cursor.execute(
				"SELECT id FROM Category WHERE name = %s", (category,)) 
			result = cursor.fetchone()
			if result:
				category_id = result[0]
			else:
				cursor.execute(
					"INSERT INTO Category (name) VALUES (%s)", (category,)) #  On duplicate key update? if not exists?
				category_id = cursor.lastrowid
			for p in products_list:
				p = self.verify_product(p)
				if p:
					p_name = p["product_name"]
					p_brand = p["brands"].split(",")[0]
					if p_brand and p_brand not in p_name:
						p_name += " " + p_brand
					p_values = (category_id, p_name,
						p["nutrition_grade_fr"], p["generic_name_fr"],
						p["stores"], p["url"])
					# change ignore. On duplicate key update? if not exists?
					querry = "INSERT IGNORE INTO Product (category_id, name, \
						nutriscore, description, shop, url) \
						VALUES (%s, %s, %s, %s, %s, %s)" # mauvaise indentation
					cursor.execute(querry, p_values)

	def fill_database(self):
		cnx = self.connect()
		cursor = cnx.cursor()
		try:
			self.create_tables(cursor)
			self.fill_tables(cursor)
			cnx.commit()
		finally:
			cursor.close()
			cnx.close()
