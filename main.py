from connectmenu import ConnectMenu


def main():
    """Launch this function to run the program"""
    with ConnectMenu() as menu:
        menu.main_menu()

if __name__ == '__main__':
    main()
