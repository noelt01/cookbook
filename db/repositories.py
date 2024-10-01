from sqlalchemy.orm import Session
from db.models import Step, Ingredient, RecipeCategories, Recipe
import db.schemas as _schemas
# from db.db import Base, engine


class StepRepo:
    
    async def create_step(db: Session, step: _schemas.StepCreate):
            db_step = Step(step_number=step.step_number,step=step.step,recipe_id=step.recipe_id)
            db.add(db_step)
            db.commit()
            db.refresh(db_step)
            return db_step
        
    def fetch_steps_by_recipe_id(db: Session,_id):
        return db.query(Step).filter_by(recipe_id=_id).all()
    
    async def delete_step(db: Session,step_id):
        db_step= db.query(Step).filter_by(id=step_id).first()
        db.delete(db_step)
        db.commit()
        
        
    async def update_step(db: Session,step_data):
        updated_step = db.merge(step_data)
        db.commit()
        return updated_step
    
    
    
class IngredientRepo:
    
    async def create_ingredient(db: Session, ingredient: _schemas.IngredientCreate):
            db_ingredient = Ingredient(name=ingredient.name,amount=ingredient.amount,measurement=ingredient.measurement,recipe_id=ingredient.recipe_id)
            db.add(db_ingredient)
            db.commit()
            db.refresh(db_ingredient)
            return db_ingredient
        
    def fetch_ingredients_by_name(db: Session,_name):
        return db.query(Ingredient).filter(Ingredient.name == _name).first()
    
    def fetch_all_ingredients(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Ingredient).offset(skip).limit(limit).all()
    
    def fetch_ingredients_by_recipe_id(db: Session,_id):
        return db.query(Ingredient).filter_by(recipe_id=_id).all()
    
    async def delete_ingredient(db: Session,ingredient_id):
        db_ingredient= db.query(Ingredient).filter_by(id=ingredient_id).first()
        db.delete(db_ingredient)
        db.commit()
    
    async def update_ingredient(db: Session,ingredient_data):
        updated_ingredient = db.merge(ingredient_data)
        db.commit()
        return updated_ingredient
    

class RecipeCategoriesRepo:
    
    async def create_category(db: Session, category: _schemas.RecipeCategoriesCreate):
            db_category = RecipeCategories(name=category.name,recipe_id=category.recipe_id)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return db_category
        
    def fetch_category_by_name(db: Session,_name):
        return db.query(RecipeCategories).filter(RecipeCategories.name == _name).first()
   
    def fetch_catagories_by_recipe_id(db: Session,_id):
        return db.query(RecipeCategories).filter_by(recipe_id=_id).all()
    
    def fetch_all_categories(db: Session, skip: int = 0, limit: int = 100):
        return db.query(RecipeCategories).offset(skip).limit(limit).all()
    
    async def delete_category(db: Session,_id:int):
        db_category= db.query(RecipeCategories).filter_by(id=_id).first()
        db.delete(db_category)
        db.commit()
        
    async def update(db: Session,category_data):
        db.merge(category_data)
        db.commit()


class RecipeRepo:
    
    async def create_recipe(db: Session, recipe: _schemas.RecipeCreate):
            db_recipe = Recipe(title=recipe.title,description=recipe.description)
            db.add(db_recipe)
            db.commit()
            db.refresh(db_recipe)
            return db_recipe
        
    def fetch_recipe_by_id(db: Session,_id):
        return db.query(Recipe).filter(Recipe.id == _id).first()
    
    def fetch_recipe_by_slug(db: Session,_slug):
        return db.query(Recipe).filter(Recipe.slug == _slug).first()
    
    def fetch_all_recipes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Recipe).offset(skip).limit(limit).all()
    
    async def delete_recipe(db: Session,_id:int):
        db_recipe= db.query(Recipe).filter_by(id=_id).first()
        db.delete(db_recipe)
        db.commit()
        
    async def update(db: Session,recipe_data):
        db.merge(recipe_data)
        db.commit()
