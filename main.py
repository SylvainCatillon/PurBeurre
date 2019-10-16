import DatabaseHandler as cdb
import ApiCommunicator as ac

def main():
	communicator = ac.ApiCommunicator()
	products_dict = communicator.dl_products()
	handler = cdb.DatabaseHandler(products_dict)
	handler.fill_database()

if __name__ == '__main__':
		main()