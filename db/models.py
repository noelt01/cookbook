from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import relationship

from db.db import Base


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    step_number = Column(Integer, nullable=False, unique=False, index=False)
    step = Column(String(200), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(step) > 0", name="step_step_length_check"),
        UniqueConstraint("step_number", "recipe_id", name="uq_step_number_recipe"),
    )

    def __repr__(self):
        return "StepModel(step_number=%s, step=%s,recipe_id=%s)" % (
            self.step_number,
            self.step,
            self.recipe_id,
        )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    amount = Column(String(5), nullable=True)
    measurement = Column(String(15), nullable=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="ingredient_name_length_check"),
        CheckConstraint("LENGTH(amount) > 0", name="ingredient_amount_length_check"),
        CheckConstraint(
            "LENGTH(measurement) > 0", name="ingredient_measurement_length_check"
        ),
    )

    def __repr__(self):
        return "IngredientModel(name=%s, amount=%s,measurement=%s,recipe_id=%s)" % (
            self.name,
            self.amount,
            self.measurement,
            self.recipe_id,
        )


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="category_name_length_check"),
        UniqueConstraint("name", name="uq_category"),
    )

    def __repr__(self):
        return "RecipeCategoriesModel(name=%s)" % (self.name)


class RecipeCategories(Base):
    __tablename__ = "recipe_categories"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("recipe_id", "category_id", name="uq_recipe_category_id"),
    )

    def __repr__(self):
        return "RecipeCategoriesModel(name=%s)" % (self.name)


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(80), nullable=False, unique=True)
    slug = Column(String(100), nullable=False)
    description = Column(String(200))
    steps = relationship(
        "Step",
        primaryjoin="Recipe.id == Step.recipe_id",
        cascade="all, delete-orphan",
        order_by="Step.step_number",
    )
    ingredients = relationship(
        "Ingredient",
        primaryjoin="Recipe.id == Ingredient.recipe_id",
        cascade="all, delete-orphan",
    )
    categories = relationship(
        "RecipeCategories",
        primaryjoin="Recipe.id == RecipeCategories.recipe_id",
        cascade="all, delete-orphan",
    )
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("LENGTH(title) > 0", name="recipe_title_length_check"),
        CheckConstraint(
            "LENGTH(description) > 0", name="recipe_description_length_check"
        ),
        UniqueConstraint("title", name="uq_recipe_title"),
        UniqueConstraint("slug", name="uq_recipe_slug"),
    )

    def __repr__(self):
        return "Recipe(title=%s, description=%s)" % (self.title, self.description)
