from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.ingredient_schema import IngredientIn, IngredientOut
from services.ingredient_crud import create_ingredient, get_ingredient_list

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post(
    "/",
    response_model=IngredientOut,
    status_code=status.HTTP_201_CREATED,
    description="Create a new ingredient"
)
def create_ingredient_api(ingredient_in: IngredientIn, db: Session = Depends(get_db)):
    try:
        ingredient = create_ingredient(db=db, ingredient_in=ingredient_in)
        return ingredient
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get(
    "/",
    response_model=List[IngredientOut],
    status_code=status.HTTP_200_OK,
    description="Get a list of all ingredients"
)
def get_ingredient_list_api(db: Session = Depends(get_db)):
    ingredients = get_ingredient_list(db=db)
    return ingredients
