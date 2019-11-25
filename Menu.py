import config
from text import Menu_text as txt
from apicommunicator import ApiCommunicator
from dbseeker import DatabaseSeeker
from dbcreator import DatabaseCreator


class Menu:
    """Use Menu.main_menu() to launch the Menu.
    The Menu guide the user through a series of events:
    -Choose a category
    -Choose between randomly selected products of this category
    -See an healthier product of the category
    -Save the subtitute"""

    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor
        self.seeker = DatabaseSeeker(self.cursor, self.cnx)
        # An instance of DatabaseCreator isn't allways needed, so
        # it will be created when needed and assigned to self.creator.
        self.creator = None

    @staticmethod
    def display_substitute(sbt_dict):
        """Uses the given dict to display the substitute's informations.
        Takes as param a dict with the following keys: name, description,
        shop, url. sbt_dict["shop"] can be an empty string. """
        if sbt_dict:
            string = txt["sbt_prs"].format(
                name=sbt_dict["name"], description=sbt_dict["description"])
            if sbt_dict["shop"]:
                string += txt["sbt_shop"].format(shop=sbt_dict["shop"])
            string += txt["sbt_url"].format(url=sbt_dict["url"])
            print(string)
        else:
            print(txt["no_sbt"])

    def get_input(self, string, input_range):
        """Asks an input with the given string, then tests if the
        input is a number, and is between 1 and the given range"""
        inp = input(string)
        try:
            inp = int(inp)
        except ValueError:
            print(txt["wrong_input"])
            return self.get_input(string, input_range)
        if inp < 1 or inp > input_range:
            print(txt["wrong_input"])
            return self.get_input(string, input_range)
        return inp

    def choose_category(self):
        """Asks the user to choose a category, by a number on input"""
        string = txt["choose_category"]
        good_categories, low_categories = self.seeker.see_categories()
        for category_dict in low_categories:
            print(txt["low_category"].format(category=category_dict["name"]))
        for i, category_dict in enumerate(good_categories):
            # i+1 because the list starts with 1 for the user
            string += "{}: {}\n".format(i+1, category_dict["name"])
        inp = self.get_input(string, len(good_categories))
        # inp-1 because the list starts with 1 for the user
        return good_categories[inp-1]["id"]

    def choose_product(self, category_id):
        """Selects randomly some products of the given category,
        and asks the user to choose one"""
        products_list = self.seeker.random_products(category_id)
        string = txt["choose_product"]
        for i, product in enumerate(products_list):
            # i+1 because the list starts with 1 for the user
            string += "{}: {}\n".format(i+1, product["name"])
        inp = self.get_input(string, len(products_list))
        # inp-1 because the list starts with 1 for the user
        return products_list[inp-1]

    def save_substitute(self, sbt_id):
        """Asks the user if he/she wants to save the substitute.
        If the input is 1, saves the substitute in the database"""
        string = txt["save_sbt"]
        inp = self.get_input(string, 2)
        if inp == 1:
            self.seeker.save_product(sbt_id)

    def search_substitute(self):
        """Runs the methods to:
        -Let the user choose a category
        -Let the user choose a product
        -Find a substitute
        -Save the substitute"""
        category_id = self.choose_category()
        product = self.choose_product(category_id)
        sbt_dict = self.seeker.find_substitute(product)
        self.display_substitute(sbt_dict)
        if sbt_dict:
            if self.seeker.is_saved(sbt_dict["id"]):
                print(txt["saved_sbt"])
            else:
                self.save_substitute(sbt_dict["id"])

    def see_favories(self):
        """Allows the user to see a list of the saved substitutes,
        then choose one of the favorites to see more details"""
        favories = self.seeker.see_favories()
        if favories:
            string = txt["choose_sbt"]
            for i, favory in enumerate(favories):
                # i+1 because the list starts with 1 for the user
                string += "{}: {}\n".format(i+1, favory["name"])
            inp = self.get_input(string, len(favories))
            # inp-1 because the list starts with 1 for the user
            self.display_substitute(favories[inp-1])
        else:
            print(txt["no_saved_sbt"])

    def prepare_database(self, categories_name, reset=False):
        """Makes a request at OpenFoodFacts to download the products
        of the given categories, and fills them in the database.
        If reset=True, the existing tables will be deleted"""
        print(txt["pls_wait"])
        if not self.creator:
            self.creator = DatabaseCreator(self.cursor, self.cnx)
        if reset:
            self.creator.reset_database()
        products_dict = ApiCommunicator.dl_products(categories_name)
        self.creator.fill_database(products_dict)
        print(txt["dl_done"])

    def update_database(self):
        """Warns the user that an update will erase all datas,
        then asks an input. If the input is 1, reset the database"""
        string = txt["update_database"]
        inp = self.get_input(string, 2)
        if inp == 1:
            self.prepare_database(config.categories_name, reset=True)

    def main_menu(self):
        """The main method of Menu. Launch this method to run the app"""
        print(txt["welcome"])
        categories_name = self.seeker.test_database()
        if categories_name:
            self.prepare_database(categories_name)
        string = txt["main_choice"]
        inp = self.get_input(string, 4)
        if inp == 1:
            self.search_substitute()
        elif inp == 2:
            self.see_favories()
        elif inp == 3:
            self.update_database()
        elif inp == 4:
            return None
        string = txt["play_again"]
        inp = self.get_input(string, 2)
        if inp == 1:
            return self.main_menu()
        return None
