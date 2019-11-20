import requests
import config
from text import ApiCommunicator_text as txt

class ApiCommunicator:

	@staticmethod
	def dl_products(categories_name):
		products_dict={}
		for category in categories_name:
			products_list = []
			nb_pages = config.nb_dl_prod//20
			for page in range(1, nb_pages+1):
				raw_result = requests.get(
					"https://fr.openfoodfacts.org/categorie/{}/{}.json".format(
						category, page))
				result = raw_result.json()
				if result["count"] < config.min_prod_in_db*3:
					print(txt["wrong_cat"].format(category=category))
					break
				products_list += result["products"]
			print(txt["cat_downloaded"].format(category=category))
			products_dict[category] = products_list
		return products_dict