import requests as req
import mysql.connector

products = {}
nb_pages = 1000//20
categories = ["jus-d-orange"]
product_keys = ["product_name", "categories", "url", "nutrition_grade_fr", "purchase_places"]

def fill_dict():
	for category in categories:
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

"""def fill_db(products_dict):
	connection = mysql.connector.connect(user= config.user, pasword = config.password, database = config.database, host = config.host)
	try:
		with connection.cursor() as cursor:
			cursor.execute("CREATE TABLE products (id SMALLINT UNSIGNED AUTO INCREMENT PRIMARY KEY, nom VARCHAR, category_id)")
			sql = "INSERT INTO products (nom, category_id) VALUES (%s,%s)"
			for product in products_dict:
				cursor.execute(sql, (product["product_name"], #product[category_id]))
"""
if __name__ == '__main__':
	fill_dict()
	print(len(products["jus-d-orange"]))

