import requests
import sqlite3

def display_data(to_display):
    for recipe in to_display:
        print(recipe['title'])


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
    display_data(data)


if __name__ == '__main__':
    main()
