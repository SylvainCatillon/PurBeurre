# PurBeurreApp
PurBeurreApp allow you to find healthier substitutes of your favorites aliments, using Open Food Facts database. https://world.openfoodfacts.org/ \
You can choose between 5 categories, then between 10 randomly chosen aliments. Once you selected an aliment, the app will search for
a healthier substitute and show you a description of the substitute, a shop where you can buy it and a like to his Open Food Facts page.
You can save your search, to find easily all of your substitutes.

# Getting started
Use the requirement.txt to install the needed package: 
`pip install -r requirements.txt`\
Please install MySQL: https://dev.mysql.com/downloads/mysql/#downloads \
Then create a data base, and change the `config.py` file to set the user and password. Choose a user who can access the data base.\
Last step before we start, `launch 'fill_database.py` to fill the data base with the datas of Open Food Facts\
Finnaly, you can launch `main.py` to start the app
