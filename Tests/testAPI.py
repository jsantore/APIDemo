# import pytest
import GetRecipeData


def test_get_data():
    test_location = 'http://www.recipepuppy.com/api/?i=onions,garlic&q=omelet'
    test_results = GetRecipeData.get_data(test_location)
    assert len(test_results) > 0


def test_get_bad_data():
    test_location = 'http://recipepuppy.com/apidev/?i=onions,garlic&q=omelet'
    test_results = GetRecipeData.get_data(test_location)
    assert type(test_results) ==list
    assert len(test_results) == 0
