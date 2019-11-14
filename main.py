from ConnectMenu import ConnectMenu

"""def main():
	menu = Menu()
	try:
		menu.main_menu()
	finally:
		menu.close_connection()"""

def new_main():
	with ConnectMenu() as menu:
		menu.main_menu()

if __name__ == '__main__':
	new_main()