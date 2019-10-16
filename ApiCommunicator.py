import requests
import config

class ApiCommunicator:


	@staticmethod
	def dl_products(products_dict={}):
		for category in config.categories_name:
			products_list = []
			for page in range(1, config.nb_pages+1):
				raw_result = requests.get("https://fr.openfoodfacts.org/categorie/{}/{}.json".format(category, page))
				result = raw_result.json()
				if result["count"] < 50:
					print("La catégorie {} n'existe pas ou ne compte pas assez de produits".format(category))
					break
				products_list += result["products"]
			print(category)
			products_dict[category] = products_list
		return products_dict