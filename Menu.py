from config import database_config as config
from ApiCommunicator import ApiCommunicator
from DatabaseSeeker import DatabaseSeeker
from DatabaseCreator import DatabaseCreator

class Menu:
	"""Use Menu.main_menu() to launch the Menu.
	The Menu guide the user through a series of event:
	-Choose a category
	-Choose between randomly selected products of this category
	-See an healthier product of the category"""

	def __init__(self):
		self.seeker = DatabaseSeeker()

	@staticmethod
	def display_substitute(sbt_dict):
		"""Use the given dict to display the substitute's informations.
		Take as param a dict with the following keys: name, description, shop,
		url. The shops can be an empty string. """
		if sbt_dict:
			string = "Voici un substitut plus sain à votre produit: \nNom: \
{}\nDescription: {}".format(sbt_dict["name"], sbt_dict["description"])
			if sbt_dict["shop"]:
				string += "\nMagasins où l'acheter: {}".format(
												sbt_dict["shop"])
			string += "\nRetrouvez ce produit sur OpenFoodFacts: {}".format(
															sbt_dict["url"])
			print(string)
		else:
			print("Il n'y a pas d'alternative plus saine à \
ce produit dans la base de données")

	def get_input(self, string, input_range):
		"""Ask an input with the given string, then test if the input is a
		number between 1 and the given range"""
		inp = input(string)
		try:
			inp = int(inp)
		except ValueError:
			print("Veuillez indiquer un chiffre")
			return self.get_input(string, input_range)
		if inp < 1 or inp > input_range:
			print("Veuillez indiquer un chiffre parmis les choix ci-dessus")
			return self.get_input(string, input_range)
		return inp

	def prepare_database(self, categories_name, reset = False):
		print("Merci de patienter quelques instants, le système télécharge \
les produits dans la base de données")
		products_dict = ApiCommunicator.dl_products(categories_name)
		creator = DatabaseCreator(products_dict)
		if reset:
			creator.reset_database()
		creator.fill_database()
		print("Données téléchargées")

	def choose_category(self):
		"""Ask the user to choose a category, by a number on input"""
		string = "Veuillez choisir une catégories parmi les suivantes, en \
indiquant le chiffre associé:\n"
		for i, category in enumerate(config["categories_name"]):
			string += "{}: {}\n".format(i+1, category) # The list start with 1 instead of 0 for the user
		inp = self.get_input(string, i+1)
		return config["categories_name"][inp-1] # The list start with 1 instead of 0 for the user

	def choose_product(self, category_name):
		"""Select randomly some products, and ask the user to choose one"""
		products_list, category_id = self.seeker.random_products(category_name) # ne pas récup category_id, et le chercher à nouveau dans find_substitute?
		string = "Veuillez choisir un produit parmi les suivants, en indiquant\
 le chiffre associé:\n"
		for i, product in enumerate(products_list):
			string += "{}: {}\n".format(i+1, product[1]) # The list start with 1 instead of 0 for the user. product[1] for the name, [0] is the id
		inp = self.get_input(string, i+1)
		return products_list[inp-1], category_id

	def save_substitute(self, sbt_dict):
		string = "Souhaitez-vous enregistrer le substitut trouvé?\n1: \
Enregistrer\n2: Ne pas enregistrer\n"
		inp = self.get_input(string, 2)
		if inp == 1:
			self.seeker.save_substitute(sbt_dict["id"])

	def search_substitute(self):
		category_name = self.choose_category()
		product, category_id = self.choose_product(category_name)
		sbt_dict = self.seeker.find_substitute(product[0], category_id)
		self.display_substitute(sbt_dict)
		if sbt_dict:
			self.save_substitute(sbt_dict)

	def see_favories(self):
		favories = self.seeker.see_favories()
		if favories:
			string = "Indiquez le chiffre associé à un substitut enregistré \
pour voir les détails:\n"
			for i, favory in enumerate(favories):
				string += "{}: {}\n".format(i+1, favory["name"]) # The list start with 1 instead of 0 for the user. product[1] for the name, [0] is the id
			inp = self.get_input(string, i+1)
			self.display_substitute(favories[inp-1])
		else:
			print("Vous n'avez pas de substitut enregistré")

	def update_database(self):
		string = "Attention, mettre à jour la base de données va supprimer vos\
 données actuelles (catégories, produits et substituts enregistrés)\n1: Mettre\
 à jour la base de données\n2: Garder les données actuelles\n"
		inp = self.get_input(string, 2)
		if inp == 1:
			self.prepare_database(config["categories_name"], reset = True)

	def main_menu(self):
		"""The main method of Menu. Launch this method to run the app."""
		print("Bonjour, bienvenue dans l'application de Pur Beurre")
		categories_name = self.seeker.test_database()
		if categories_name:
			self.prepare_database(categories_name)
		string = "1: Quel aliment souhaitez vous remplacer\n2: Retrouver mes \
aliments substitués\n3: Mettre à jour la base de données\n"
		inp = self.get_input(string, 3)
		if inp == 1:
			self.search_substitute()
		elif inp == 2:
			self.see_favories()
		elif inp == 3:
			self.update_database()
		string = "1: Retourner au menu principal\n2: Quitter\n"
		inp = self.get_input(string, 2)
		if inp == 1:
			return self.main_menu()

