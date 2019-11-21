# PurBeurreApp
PurBeurreApp allow you to find healthier substitutes to your favorites aliments, using Open Food Facts database. https://world.openfoodfacts.org/ \
You can choose between 5 categories, then between 10 randomly chosen aliments. Once you selected an aliment, the app will search for
a healthier substitute and show you a description of the substitute, a shop where you can buy it and a link to its Open Food Facts page.
You can save your search, to find easily all of your substitutes.

# Getting started
Use the requirement.txt to install the needed package: 
`pip install -r requirements.txt`\
Please install MySQL: https://dev.mysql.com/downloads/mysql/#downloads \
Then create a data base, and change the `config.py` file to set the user, the password and the name of the database. Please use an empty database, and choose a user who can access the data base.\
Finnaly, you can launch `main.py` to start the app

You can change some variables in `config.py`:
* *connection_config*: The settings of the database connection
* *categories_name*: The categories used for the program. Please use categories wich exist on https://fr.openfoodfacts.org/categories
* *nb_proposed_prod*: The number of products proposed to the user at each search
* *min_prod_in_db*: The minimum products accepted per categories in the database. Must be more than nb_proposed_prod. If the category doesn't contain enough products, the category isn't inserted in the database
* *nb_dl_prod*: The number of downloaded products per category

You can also change text.py if you want to change the displayed texts of the program

# Enjoy!
