from pydantic import BaseModel
from typing import Optional, List
from enums.countability import Countability

class IngredientIn(BaseModel):
    ingredient_name: str
    estimated_shelf_life: Optional[int] = None
    countability: Countability
    ingredienttag_ids: List[int] = []

class IngredientOut(BaseModel):
    ingredient_id: int
    ingredient_name: str
    estimated_shelf_life: Optional[int] = None
    countability: Countability
    ingredienttag_ids: List[int] = []

    class Config:
        orm_mode = True