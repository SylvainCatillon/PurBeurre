from Menu import Menu

def main():
	menu = Menu()
	try:
		menu.main_menu()
	finally:
		menu.close_connection()

if __name__ == '__main__':
	main()