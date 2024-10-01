from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Recipe, Ingredient, RecipeCategories, Step, Category
from db.schemas import (
    RecipeCreate,
    IngredientCreate,
    RecipeCategoriesCreate,
    StepCreate,
    CategoryCreate,
)


def check_existing_recipe(db: Session, recipe_data: RecipeCreate):
    existing_recipe = (
        db.query(Recipe)
        .filter((Recipe.slug == recipe_data.slug) | (Recipe.title == recipe_data.title))
        .first()
    )

    if existing_recipe:
        if existing_recipe.title == recipe_data.title:
            detail_msg = "Recipe with this title exists"
        else:
            detail_msg = "Recipe with this Slug exists"

        raise HTTPException(status_code=400, detail=detail_msg)


def check_existing_ingredient(db: Session, ingredient_data: IngredientCreate):
    existing_ingredient = (
        db.query(Ingredient)
        .filter(
            (Ingredient.name == ingredient_data.name)
            and (Ingredient.recipe_id == ingredient_data.recipe_id)
        )
        .first()
    )

    if existing_ingredient:
        if (
            existing_ingredient.name == ingredient_data.name
            and existing_ingredient.recipe_id == ingredient_data.recipe_id
        ):
            detail_msg = "Ingredient exists for recipe ID"

            raise HTTPException(status_code=400, detail=detail_msg)


def check_existing_category(db: Session, category_data: CategoryCreate):
    existing_category = (
        db.query(Category).filter((Category.name == category_data.name)).first()
    )

    if existing_category:
        if existing_category.name == category_data.name:
            detail_msg = "Category exists"

            raise HTTPException(status_code=400, detail=detail_msg)


def check_existing_recipe_categories(
    db: Session, category_data: RecipeCategoriesCreate
):
    existing_category = (
        db.query(RecipeCategories)
        .filter(
            (RecipeCategories.category_id == category_data.category_id)
            and (RecipeCategories.recipe_id == category_data.recipe_id)
        )
        .first()
    )

    if existing_category:
        if (
            existing_category.category_id == category_data.category_id
            and existing_category.recipe_id == category_data.recipe_id
        ):
            detail_msg = "Category exists for recipe ID"

            raise HTTPException(status_code=400, detail=detail_msg)


def check_existing_step(db: Session, step_data: StepCreate):
    existing_step = (
        db.query(Step)
        .filter(
            (Step.recipe_id == step_data.recipe_id)
            and (Step.step_number == step_data.step_number)
        )
        .first()
    )

    if existing_step:
        if (
            existing_step.recipe_id == step_data.recipe_id
            and existing_step.step_number == step_data.step_number
        ):
            detail_msg = "Step exists for recipe ID"

            raise HTTPException(status_code=400, detail=detail_msg)
