Menu_text = dict(
	welcome = "Bonjour, bienvenue dans l'application de Pur Beurre",

	# 1 = find subtitute, 2 = see favories, 3 = update database, 4 = quitt
	main_choice = "1: Quel aliment souhaitez vous remplacer\n2: Retrouver mes \
aliments substitués\n3: Mettre à jour la base de données\n4: Quitter\n",

	# 1 = main menu, 2 = quit
	play_again = "1: Retourner au menu principal\n2: Quitter\n",

	# Your sentence must contains {name} at the place wich you want to display
	# the name of the substitut, and {description} at the place wich you want 
	# to display its description
	sbt_prs = "Voici un substitut plus sain à votre produit: \nNom: \
{name}\nDescription: {description}",
	# Must contains {shop}
	sbt_shop = "\nMagasins où l'acheter: {shop}",
	# Must contains {url}
	sbt_url = "\nRetrouvez ce produit sur OpenFoodFacts: {url}",

	low_category = "La catégorie {category} ne contient pas assez de produits \
pour être utilisée. Essayez de mettre à jour la base de données, ou d'enlever \
cette catégorie dans le fichier de configuration",  # Must contains {category}
	saved_sbt = "Ce substitut est déjà enregistré dans votre base de données",
	no_sbt = "Il n'y a pas d'alternative plus saine à ce produit dans la \
base de données",
	wrong_input = "Veuillez indiquer un chiffre parmis les choix ci-dessus",
	pls_wait = "Merci de patienter quelques instants, le système télécharge \
les produits dans la base de données",
	dl_done = "Données téléchargées",
	choose_category = "Veuillez choisir une catégories parmi les suivantes, \
en indiquant le chiffre associé:\n",
	choose_product = "Veuillez choisir un produit parmi les suivants, \
en indiquant le chiffre associé:\n",
	save_sbt = "Souhaitez-vous enregistrer le substitut trouvé?\n1: \
Enregistrer\n2: Ne pas enregistrer\n", # 1 = save, 2 = not save
	choose_sbt = "Indiquez le chiffre associé à un substitut enregistré \
pour voir les détails:\n",
	no_saved_sbt = "Vous n'avez pas de substitut enregistré",
	update_database = "Attention, mettre à jour la base de données va \
supprimer vos données actuelles (catégories, produits et substituts \
enregistrés)\n1: Mettre à jour la base de données\n2: Garder les données \
actuelles\n"  # 1 = update, 2 = keep the data
 )

ApiCommunicator_text = dict(
	wrong_cat = "La catégorie {category} n'existe pas ou ne compte pas \
assez de produits", # Must contains {category}
	cat_downloaded = "{category} téléchargé(e)s" # Must contains {category}
)
