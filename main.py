from ApiCommunicator import ApiCommunicator
from DatabaseSeeker import DatabaseSeeker
from DatabaseHandler import DatabaseHandler
from Menu import Menu

def main():
	seeker = DatabaseSeeker()
	categories_name = seeker.test_database()
	if categories_name:
		products_dict = ApiCommunicator.dl_products(categories_name)
		handler = DatabaseHandler(products_dict)
		handler.fill_database()
	menu = Menu()
	menu.choose_category()
	#product_id, category_id = seeker.temp_random_product()
	#sbt_dict = seeker.find_substitute(product_id, category_id)
	#Menu.display_substitute(sbt_dict)


if __name__ == '__main__':
		main()