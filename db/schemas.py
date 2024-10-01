from typing import List, Optional, Annotated
from pydantic import BaseModel, StringConstraints


class StepBase(BaseModel):
    step_number: int
    step: str
    recipe_id: int


class StepCreate(StepBase):
    pass


class StepReturn(StepBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryReturn(CategoryBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class RecipeCategoriesBase(BaseModel):
    category_id: int
    recipe_id: int


class RecipeCategoriesCreate(RecipeCategoriesBase):
    pass


class RecipeCategoriesReturn(RecipeCategoriesBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class IngredientBase(BaseModel):
    name: str
    amount: str
    measurement: Optional[str] = None
    recipe_id: int


class IngredientCreate(IngredientBase):
    pass


class IngredientReturn(IngredientBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    slug: Annotated[str, StringConstraints(min_length=1)]


class RecipeCreate(RecipeBase):
    pass


class RecipeReturn(RecipeBase):
    id: int
    ingredients: Optional[List[IngredientReturn]]
    steps: Optional[List[StepReturn]]
    categories: Optional[List[RecipeCategoriesReturn]]

    class Config:
        # orm_mode = True
        from_attributes = True
