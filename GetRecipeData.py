import requests
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5 import QtWidgets
import sys

class RecipeWindow(QWidget):
    def __init__(self, to_display):
        super().__init__()
        self.data_to_display = to_display
        self.data_item_displayed = 0
        current_data = self.data_to_display[self.data_item_displayed]
        main_layout = QtWidgets.QVBoxLayout()
        top_label = QLabel("Recipe Name:")
        main_layout.addWidget(top_label)
        self.title_display = QLineEdit()
        self.title_display.setReadOnly(True)
        self.title_display.setText(current_data['title'])
        main_layout.addWidget(self.title_display)
        ing_label = QLabel("Uses these ingredients")
        main_layout.addWidget(ing_label)
        self.ing_display = QLineEdit()
        self.ing_display.setReadOnly(True)
        main_layout.addWidget(self.ing_display)
        self.ing_display.setText(current_data['ingredients'])
        get_next = QPushButton("Get Next Recipe")
        main_layout.addWidget(get_next)
        self.setLayout(main_layout)
        get_next.pressed.connect(self.show_next_recipe)

    def show_next_recipe(self):
        self.data_item_displayed += 1;
        # what could possibly go wrong!??!
        current_data = self.data_to_display[self.data_item_displayed]
        self.title_display.setText(current_data['title'])
        self.ing_display.setText(current_data['ingredients'])






def display_data(to_display):
   window = RecipeWindow(to_display)
   return window


def get_data(location):
    response = requests.get(location)
    if response.status_code != 200:
        return []
    data = response.json()
    return data['results']


def save_data(recipes:list, cursor:sqlite3.Cursor):
    for recipe in recipes:
        cursor.execute("INSERT INTO recipes(title, web_address, ingredients) VALUES (?,?,?);",
                       (recipe['title'], recipe['href'], recipe['ingredients']))


def setup_database(cursor:sqlite3.Cursor):
    create_statement = """CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    title TEXT,
    web_address TEXT,
    ingredients TEXT);"""
    cursor.execute(create_statement)

def get_params():
    ingredients = input("what ingredients shall we include? (comma separated)")
    recipe_type = input("What kind of recipe shall we look for:")
    return ingredients, recipe_type


def main():
    app = QApplication(sys.argv)
    params = get_params()
    loc = f"http://www.recipepuppy.com/api/?i={params[0]}&q={params[1]}"
    print(loc)
    connection = sqlite3.connect("recipes.db")
    cursor = connection.cursor()
    setup_database(cursor)
    data = get_data(loc)
    save_data(data, cursor)
    connection.commit()
    connection.close()
    window = display_data(data)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
