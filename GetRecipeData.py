import requests


def display_data(to_display):
    for recipe in to_display:
        print(recipe['title'])


def get_data(location):
    response = requests.get(location)
    if response.status_code != 200:
        return []
    data = response.json()
    return data['results']


def get_params():
    ingredients = input("what ingredients shall we include? (comma separated)")
    recipe_type = input("What kind of recipe shall we look for:")
    return ingredients, recipe_type


def main():
    params = get_params()
    loc = f"http://www.recipepuppy.com/api/?i={params[0]}&q={params[1]}"
    print(loc)
    data = get_data(loc)
    display_data(data)


if __name__ == '__main__':
    main()
