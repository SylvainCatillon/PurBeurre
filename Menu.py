from config import database_config as config
from DatabaseSeeker import DatabaseSeeker

class Menu:

	def __init__(self):
		self.seeker = DatabaseSeeker()

	@staticmethod
	def display_substitute(sbt_dict):
		if sbt_dict:
			string = "Voici un substitut plus sain à votre produit: \nNom: {}\nDescription: {}".format(sbt_dict["name"], sbt_dict["description"])
			if sbt_dict["shop"]:
				string += "\nMagasins où l'acheter: {}".format(sbt_dict["shop"])
			string += "\nRetrouvez ce produit sur OpenFoodFacts: {}".format(sbt_dict["url"])
			print(string)

	def get_input(self, string, input_range):
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


	def choose_category(self):
		string = "Veuillez choisir une catégories parmi les suivantes, en indiquant le chiffre associé:\n"
		for i, category in enumerate(config["categories_name"]):
			string += "{}: {}\n".format(i+1, category) # The list start with 1 instead of 0 for the user
		inp = self.get_input(string, i+1)
		return config["categories_name"][inp-1] # The list start with 1 instead of 0 for the user

	def choose_product(self, category_name):
		products_list, category_id = self.seeker.random_products(category_name) # ne pas récup category_id, et le chercher à nouveau dans find_substitute?
		string = "Veuillez choisir un produit parmi les suivants, en indiquant le chiffre associé:\n"
		for i, product in enumerate(products_list):
			string += "{}: {}\n".format(i+1, product[1]) # The list start with 1 instead of 0 for the user. product[1] for the name, [0] is the id
		inp = self.get_input(string, i+1)
		return products_list[inp-1], category_id

	def main_menu(self):
		category_name = self.choose_category()
		product, category_id = self.choose_product(category_name)
		sbt_dict = self.seeker.find_substitute(product[0], category_id)
		self.display_substitute(sbt_dict)

