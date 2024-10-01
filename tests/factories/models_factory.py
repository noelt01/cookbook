from faker import Faker
from itertools import count


faker = Faker()

id_counter = count(start=1)

# class Recipe:
#     def __init__(self, id_: int, title: str, description: str):
#         self.id_ = id
#         self.name = title
#         self.description = description
#         self.categories = []
#         self.ingredients = []
#         self.steps = []


def get_random_recipe_dict(id_: int = None):
    id_counter = count(start=1)
    id_ = next(id_counter)
    return {
        "id": id_,
        "title": faker.word(),
        "slug": faker.slug(),
        "description": faker.text(15),
        "categories": [],
        "ingredients": [],
        "steps": [],
    }


def get_random_ingredient_dict(id_: int = None):
    id_counter = count(start=1)
    id_ = next(id_counter)
    return {
        "id": id_,
        "name": faker.word(),
        "amount": faker.text(5),
        "measurement": faker.text(10),
        "recipe_id": faker.random_int(1, 1),
    }


def get_random_category_dict(id_: int = None):
    id_counter = count(start=1)
    id_ = next(id_counter)
    return {
        "id": id_,
        "name": faker.word(),
    }


def get_random_recipe_categories_dict(id_: int = None):
    id_counter = count(start=1)
    id_ = next(id_counter)
    return {
        "id": id_,
        "recipe_id": faker.random_int(1, 10),
        "category_id": faker.random_int(1, 10),
    }


def get_random_step_dict(id_: int = None):
    id_counter = count(start=1)
    id_ = next(id_counter)
    return {
        "id": id_,
        "step_number": faker.random_int(1, 5),
        "step": faker.text(),
        "recipe_id": faker.random_int(1, 10),
    }
