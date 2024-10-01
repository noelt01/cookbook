from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.schemas import (
    RecipeReturn,
    RecipeCreate,
    IngredientReturn,
    IngredientCreate,
    CategoryCreate,
    CategoryReturn,
    StepReturn,
    StepCreate,
    RecipeCategoriesReturn,
    RecipeCategoriesCreate,
)
from db.models import Recipe, Ingredient, RecipeCategories, Step, Category
from db.db import SessionLocal, get_db_session
from db.repositories import IngredientRepo
from app.utils.recipe_utils import (
    check_existing_recipe,
    check_existing_ingredient,
    check_existing_category,
    check_existing_recipe_categories,
    check_existing_step,
)


router = APIRouter()
db = SessionLocal()


@router.get("/recipe", response_model=List[RecipeReturn], tags=["Recipe"])
def get_all_recipes(db: Session = Depends(get_db_session)):
    try:
        recipes = db.query(Recipe).all()
        return recipes
    except Exception as e:
        # logger.error(f"Unexpected error while retriving recipes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recipe/{recipe_slug}", response_model=RecipeReturn, tags=["Recipe"])
def get_recipe_by_slug(recipe_slug: str, db: Session = Depends(get_db_session)):
    try:
        recipe = db.query(Recipe).filter(Recipe.slug == recipe_slug).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe does not exist")
        return recipe
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/recipe", response_model=RecipeReturn, status_code=201, tags=["Recipe"])
def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db_session)):
    check_existing_recipe(db, recipe_data)

    try:
        new_recipe = Recipe(**recipe_data.model_dump())
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/ingredient",
    response_model=IngredientReturn,
    status_code=201,
    tags=["Ingredients"],
)
def create_ingredient(
    ingredient_data: IngredientCreate, db: Session = Depends(get_db_session)
):
    check_existing_ingredient(db, ingredient_data)

    try:
        new_ingredient = Ingredient(**ingredient_data.model_dump())
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/ingredient/{recipe_slug}",
    response_model=List[IngredientReturn],
    tags=["Ingredients"],
)
def get_ingredient_by_recipe_slug(
    recipe_slug: str, db: Session = Depends(get_db_session)
):
    try:
        recipe = db.query(Recipe).filter(Recipe.slug == recipe_slug).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe does not exist")

        ingredients = (
            db.query(Ingredient).filter(Ingredient.recipe_id == recipe.id).all()
        )
        return ingredients

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/category/{recipe_slug}",
    response_model=List[RecipeCategoriesReturn],
    tags=["Category"],
)
def get_categories_by_recipe_slug(recipe_slug, db: Session = Depends(get_db_session)):
    try:
        recipe = db.query(Recipe).filter(Recipe.slug == recipe_slug).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe does not exist")

        categories = (
            db.query(RecipeCategories)
            .filter(RecipeCategories.recipe_id == recipe.id)
            .all()
        )
        return categories

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/category{recipe_slug}",
    response_model=RecipeCategoriesReturn,
    status_code=201,
    tags=["Category"],
)
def add_recipe_category(
    recipe_slug: str, category_name: str, db: Session = Depends(get_db_session)
):
    category_data = db.query(Category).filter(Category.name == category_name).first()
    recipe_data = db.query(Recipe).filter(Recipe.slug == recipe_slug).first()
    # check_existing_recipe_categories(db, recipe_category_data)

    try:
        new_category = RecipeCategories(
            recipe_id=recipe_data.id, category_id=category_data.id
        )
        check_existing_recipe_categories(db, new_category)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/category", response_model=List[CategoryReturn], tags=["Category"])
def get_all_categories(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        # logger.error(f"Unexpected error while retriving categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/category", response_model=CategoryReturn, status_code=201, tags=["Category"]
)
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db_session)
):
    check_existing_category(db, category_data)

    try:
        new_category = Category(**category_data.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/steps/{recipe_slug}",
    response_model=List[StepReturn],
    tags=["Steps"],
)
def get_steps_by_recipe_slug(
    recipe_slug: str, db: Session = Depends(get_db_session)
):
    try:
        recipe = db.query(Recipe).filter(Recipe.slug == recipe_slug).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe does not exist")

        steps = (
            db.query(Step).filter(Step.recipe_id == recipe.id).all()
        )
        return steps

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/step", response_model=StepReturn, status_code=201, tags=["Steps"])
def create_step(step_data: StepCreate, db: Session = Depends(get_db_session)):
    check_existing_step(db, step_data)

    try:
        new_step = Step(**step_data.model_dump())
        db.add(new_step)
        db.commit()
        db.refresh(new_step)
        return new_step
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
