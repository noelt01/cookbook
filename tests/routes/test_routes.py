import json
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from db.models import Recipe, Ingredient, RecipeCategories, Step, Category
from tests.factories.models_factory import (
    get_random_recipe_dict,
    get_random_ingredient_dict,
    get_random_category_dict,
    get_random_recipe_categories_dict,
    get_random_step_dict,
)


class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


client = TestClient(app)


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_read_main():
    response = client.get("/recipe")
    assert response.status_code == 200


@pytest.mark.parametrize("recipe", [get_random_recipe_dict() for _ in range(3)])
def test_unit_get_single_recipe_sucessfully(client, monkeypatch, recipe):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    response = client.get(f"/recipe/{recipe['slug']}")
    assert response.status_code == 200
    assert response.json() == recipe


@pytest.mark.parametrize("recipe", [get_random_recipe_dict() for _ in range(3)])
def test_unit_get_single_recipe_not_found(client, monkeypatch, recipe):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    response = client.get(f"/recipe/{recipe['slug']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe does not exist"}


@pytest.mark.parametrize("recipe", [get_random_recipe_dict() for _ in range(3)])
def test_unit_get_single_recipe_with_internal_server_error(client, monkeypatch, recipe):
    def mock_create_recipe_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_create_recipe_exception)
    response = client.get(f"/recipe/{recipe['slug']}")
    assert response.status_code == 500


def test_unit_get_all_recipe_sucessfully(client, monkeypatch):
    recipe = [get_random_recipe_dict(i) for i in range(5)]
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(recipe))
    response = client.get("/recipe")
    assert response.status_code == 200
    assert response.json() == recipe


def test_unit_get_all_recipe_returns_empty(client, monkeypatch):
    recipe = []
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(recipe))
    response = client.get("/recipe")
    assert response.status_code == 200
    assert response.json() == recipe


def test_unit_get_recipe_all_with_internal_server_error(client, monkeypatch):
    def mock_creaate_recipe_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_creaate_recipe_exception)
    response = client.get("/recipe")
    assert response.status_code == 500


def test_unit_create_new_recipe_successfully(client, monkeypatch):
    recipe = get_random_recipe_dict()

    Recipe()
    for key, value in recipe.items():
        monkeypatch.setattr(Recipe, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = recipe.copy()
    body.pop("id")
    response = client.post("/recipe", json=body)
    assert response.status_code == 201
    assert response.json() == recipe


@pytest.mark.parametrize(
    "existing_recipe, recipe_data, expected_detail",
    [
        (True, get_random_recipe_dict(), "Recipe with this title exists"),
        (True, get_random_recipe_dict(), "Recipe with this slug exists"),
    ],
)
def test_unit_create_new_recipe_existing(
    client, monkeypatch, existing_recipe, recipe_data, expected_detail
):
    def mock_check_existing_recipe(db, recipe_data):
        if existing_recipe:
            raise HTTPException(status_code=400, detail=expected_detail)

    monkeypatch.setattr(
        "app.routes.recipes.check_existing_recipe",
        mock_check_existing_recipe,
    )

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    body = recipe_data.copy()
    body.pop("id")
    response = client.post("/recipe", json=body)
    assert response.status_code == 400

    if expected_detail:
        assert response.json() == {"detail": expected_detail}


def test_unit_create_new_recipe_with_internal_server_error(client, monkeypatch):
    recipe = get_random_recipe_dict()

    Recipe()

    def mock_create_recipe_exception(*args, **kwargs):
        raise Exception("Internal server error")

    for key, value in recipe.items():
        monkeypatch.setattr(Recipe, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_create_recipe_exception)

    body = recipe.copy()
    body.pop("id")
    response = client.post("/recipe", json=body)
    assert response.status_code == 500


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_ingredient_by_recipe_successfully(
    client, monkeypatch, recipe: Recipe
):
    slug = recipe.get("slug")
    ingredients = [get_random_ingredient_dict(i) for i in range(5)]
    recipe = Dict2Class(recipe)
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(ingredients))

    response = client.get(f"/ingredient/{slug}")
    assert response.status_code == 200
    assert response.json() == ingredients


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_ingredients_by_recipe_not_found(client, monkeypatch, recipe: Recipe):
    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(Dict2Class(recipe)))
    response = client.get(f"/ingredient/{slug}")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_ingredient_all_with_internal_server_error(
    client, monkeypatch, recipe
):
    def mock_create_ingredient_exception(*args, **kwargs):
        raise Exception("Internal server error")

    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_create_ingredient_exception)
    response = client.get(f"/ingredient/{slug}")
    assert response.status_code == 500


def test_unit_create_new_ingredient_successfully(client, monkeypatch):
    ingredient = get_random_ingredient_dict()

    Ingredient()
    for key, value in ingredient.items():
        monkeypatch.setattr(Ingredient, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = ingredient.copy()
    body.pop("id")
    response = client.post("/ingredient", json=body)
    assert response.status_code == 201
    assert response.json() == ingredient


def test_unit_get_all_categories_sucessfully(client, monkeypatch):
    category = [get_random_category_dict(i) for i in range(5)]
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(category))
    response = client.get("/category")
    assert response.status_code == 200
    assert response.json() == category


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_category_by_recipe_successfully(client, monkeypatch, recipe: Recipe):
    slug = recipe.get("slug")
    categories = [get_random_recipe_categories_dict(i) for i in range(5)]
    recipe = Dict2Class(recipe)
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(categories))

    response = client.get(f"/category/{slug}")
    assert response.status_code == 200
    assert response.json() == categories


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_category_by_recipe_not_found(client, monkeypatch, recipe: Recipe):
    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    response = client.get(f"/category/{slug}")
    assert response.status_code == 404
    

@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_category_by_recipe_with_internal_server_error(
    client, monkeypatch, recipe
):
    def mock_create_recipe_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr(
        "sqlalchemy.orm.Query.all", mock_create_recipe_category_exception
    )
    response = client.get(f"/category/{slug}")
    assert response.status_code == 500


def test_unit_create_new_category_successfully(client, monkeypatch):
    category = get_random_category_dict()

    Category()
    for key, value in category.items():
        monkeypatch.setattr(Category, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = category.copy()
    response = client.post("/category", json=body)
    assert response.status_code == 201
    assert response.json() == body


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_steps_by_recipe_successfully(
    client, monkeypatch, recipe: Recipe
):
    slug = recipe.get("slug")
    steps = [get_random_step_dict(i) for i in range(5)]
    recipe = Dict2Class(recipe)
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(steps))

    response = client.get(f"/steps/{slug}")
    assert response.status_code == 200
    assert response.json() == steps


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_steps_by_recipe_not_found(client, monkeypatch, recipe: Recipe):
    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(Dict2Class(recipe)))
    response = client.get(f"/steps/{slug}")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("recipe", [get_random_recipe_dict()])
def test_unit_get_steps_all_with_internal_server_error(
    client, monkeypatch, recipe
):
    def mock_create_step_exception(*args, **kwargs):
        raise Exception("Internal server error")

    slug = recipe.get("slug")
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(recipe))
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_create_step_exception)
    response = client.get(f"/steps/{slug}")
    assert response.status_code == 500


def test_unit_create_new_step_successfully(client, monkeypatch):
    step = get_random_step_dict()

    Step()
    for key, value in step.items():
        monkeypatch.setattr(Step, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = step.copy()
    body.pop("id")
    response = client.post("/step", json=body)
    assert response.status_code == 201
    assert response.json() == step
