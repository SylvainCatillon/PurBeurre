class DatabaseCreator:

	
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

	def __init__(self, cursor, cnx):
		self.cursor = cursor
		self.cnx = cnx

	def create_tables(self):
		"""Creates in the database the tables needed for the program"""
		for table in self.TABLES_LIST:
			querry = "CREATE TABLE IF NOT EXISTS " + table + " ENGINE=INNODB"
			self.cursor.execute(querry)

	def verify_product(self, product):
		"""Verifies if the product have the informations needed"""
		for tag in self.PRODUCT_TAGS:
			if tag not in product.keys() or not product[tag]:
				if tag in ("stores", "brands"):
					product[tag] = ""
				else:
					return None
		return product

	def insert_product(self, product, category_id):
		p_name = product["product_name"]
		# If there is brands indicated for the product, the first of
		# them will be used to complement the name of the product
		p_brand = product["brands"].split(",")[0]
		if p_brand and p_brand not in p_name:
			p_name += " " + p_brand
		p_values = (category_id, p_name,
			product["nutrition_grade_fr"], product["generic_name_fr"],
			product["stores"], product["url"])
		# change ignore. On duplicate key update? if not exists?
		querry = "INSERT IGNORE INTO Product (category_id, name, \
			nutriscore, description, shop, url) \
			VALUES (%s, %s, %s, %s, %s, %s)" # mauvaise indentation?
		self.cursor.execute(querry, p_values)

	def fill_tables(self, products_dict):
		cursor = self.cursor
		for category, products_list in products_dict.items():
			cursor.execute(
				"SELECT id FROM Category WHERE name = %s", (category,)) 
			result = cursor.fetchone()
			if result:
				category_id = result["id"]
			else:
				cursor.execute(
					"INSERT INTO Category (name) VALUES (%s)", (category,))
				category_id = cursor.lastrowid
			for product in products_list:
				product = self.verify_product(product)
				if product:
					self.insert_product(product, category_id)

	def fill_database(self, products_dict):
		cursor = self.cursor
		self.create_tables()
		self.fill_tables(products_dict)
		self.cnx.commit()

	def reset_database(self):
		cursor = self.cursor
		cursor.execute("DROP TABLE Favory")
		cursor.execute("DROP TABLE Product")
		cursor.execute("DROP TABLE Category")
		self.cnx.commit()