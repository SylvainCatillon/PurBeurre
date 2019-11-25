import requests

import config
from text import ApiCommunicator_text as txt


class ApiCommunicator:
    """Use this class to download products from fr.openfoodfacts.org"""

    @staticmethod
    def dl_products(categories_name):
        """Static method. Downloads products from fr.openfoodfacts.org.
        Takes as argument a list of categories name, and returns
        a dict of products with categories as keys.
        For each category:
        -Calculates the number of pages needed (20 products per pages)
        -Prints a message and cancel dl if the category does not contains
        enough products
        -If the dl is successful, prints a message and puts the products
        in a dictionnary, with the category as key"""
        products_dict = {}
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
