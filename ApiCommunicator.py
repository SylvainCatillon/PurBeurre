import requests
from config import api_config as config

class ApiCommunicator:


	"""@staticmethod
	def dl_products(products_dict={}):
		for category in config["categories_name"]:
			products_list = []
			nb_pages = config["nb_products"]//20
			for page in range(1, nb_pages+1):
				raw_result = requests.get("https://fr.openfoodfacts.org/categorie/{}/{}.json".format(category, page))
				result = raw_result.json()
				if result["count"] < 50:
					print("La catégorie {} n'existe pas ou ne compte pas assez de produits".format(category))
					break
				products_list += result["products"]
			print(category)
			products_dict[category] = products_list
		return products_dict"""

	@staticmethod
	def dl_products(categories_name):
		products_dict={}
		for category in categories_name:
			products_list = []
			nb_pages = config["nb_products"]//20
			for page in range(1, nb_pages+1):
				raw_result = requests.get("https://fr.openfoodfacts.org/categorie/{}/{}.json".format(category, page))
				result = raw_result.json()
				if result["count"] < 50: # mettre option dans config
					print("La catégorie {} n'existe pas ou ne compte pas assez de produits".format(category))
					break
				products_list += result["products"]
			print(category)
			products_dict[category] = products_list
		return products_dict