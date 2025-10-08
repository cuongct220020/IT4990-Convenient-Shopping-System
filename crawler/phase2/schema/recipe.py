from typing import List, Optional
from pydantic import BaseModel

# Define schema corresponds to database payload, base on Pydantic
class CountableIngredient(BaseModel):
    ingredient_name: str
    quantity: Optional[int] = None

class UncountableIngredient(BaseModel):
    ingredient_name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

class Recipe(BaseModel):
    recipe_name: str
    default_servings: Optional[int] = None
    instructions: str
    countable_ingredients: List[CountableIngredient]
    uncountable_ingredients: List[UncountableIngredient]