import DatabaseHandler as dbh
import ApiCommunicator as ac
import DatabaseSeeker as dbs

def main():
	#products_dict = ac.ApiCommunicator.dl_products()
	#handler = dbh.DatabaseHandler(products_dict)
	#handler.fill_database()
	seeker = dbs.DatabaseSeeker()
	product_id, category_id = seeker.temp_random_product()
	print(seeker.find_substitute(product_id, category_id))

if __name__ == '__main__':
		main()