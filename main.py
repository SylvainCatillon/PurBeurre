import DatabaseHandler as dbh
import ApiCommunicator as ac
import DatabaseSeeker as dbs
import Menu

def main():
	seeker = dbs.DatabaseSeeker()
	categories_name = seeker.test_database()
	if categories_name:
		products_dict = ac.ApiCommunicator.dl_products(categories_name)
		handler = dbh.DatabaseHandler(products_dict)
		handler.fill_database()
	product_id, category_id = seeker.temp_random_product()
	sbt_dict = seeker.find_substitute(product_id, category_id)
	Menu.Menu.display_substitute(sbt_dict)


if __name__ == '__main__':
		main()