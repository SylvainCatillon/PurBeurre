import openfoodfacts

products = {} #  'category': [products]
nb_pages = 1000//20
categories = ["jus-d-orange"]

"""categories = openfoodfacts.facets.get_categories()
fr_categories = [category for category in categories
				if category['id'][:2] == "fr"
				and category['products'] > 500]"""

def fill_products():
	for category in categories:
		l = []
		for nb in range(nb_pages):
			l += openfoodfacts.products.get_by_category(category, page = nb+1)
		products[category] =  l

if __name__ == "main":
	fill_products()
	print(len(products["jus-d-orange"]))