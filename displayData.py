from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import PyQt5
from PyQt5.QtCore import Qt
import sqlite3
import sys


class RecipeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QtWidgets.QHBoxLayout()
        self.list_control = QtWidgets.QListWidget()
        main_layout.addWidget(self.list_control)
        data_display_layout = QtWidgets.QVBoxLayout()
        main_layout.addItem(data_display_layout)
        self.setLayout(main_layout)

    def display_data(self, recipe_data:list):
        for recipe in recipe_data:
            current_item = QtWidgets.QListWidgetItem(recipe[0], self.list_control)
            current_item.setData(Qt.UserRole, recipe[0])


def get_filtered_data(cursor: sqlite3.Cursor):
    ingredients, ingredients_ok = QtWidgets.QInputDialog.getText(None, "Choose Ingredients",
                                                                 "choose ingredient to filter data")
    sql_select = f"SELECT title FROM recipes WHERE ingredients LIKE '%{ingredients}%';"
    print(sql_select)
    results = cursor.execute(sql_select)
    return results


def main():
    app = QApplication(sys.argv)
    connection = sqlite3.connect("recipes.db")
    cursor = connection.cursor()
    recipes = get_filtered_data(cursor)
    window = RecipeWindow()
    window.display_data(recipes)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
