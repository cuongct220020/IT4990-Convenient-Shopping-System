from pydantic import BaseModel
from typing import List, Optional

class CountableIngredient(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: int

class UncountableIngredient(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: int
    unit: str

class RecipeIn(BaseModel):
    recipe_name: str
    default_servings: int
    instructions: str
    countable_ingredients: List[CountableIngredient]
    uncountable_ingredients: List[UncountableIngredient]

class RecipeOut(BaseModel):
    recipe_id: int
    recipe_name: str
    default_servings: int
    instructions: str
    countable_ingredients: List[CountableIngredient]
    uncountable_ingredients: List[UncountableIngredient]