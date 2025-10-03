from sqlalchemy.orm import Session
from models.ingredient import Ingredient, IngredientTag
from schemas.ingredient_schema import IngredientIn

"""
Create a new ingredient in the database

Args:
    db (Session): database session
    ingredient_in (IngredientIn): input data for the new ingredient
    
Returns:
    Ingredient: the newly created ingredient
    
Raises:
    ValueError: if an ingredient with the same name already exist 
"""
def create_ingredient(db: Session, ingredient_in: IngredientIn) -> Ingredient:
    existing = db.query(Ingredient).filter(
        Ingredient.ingredient_name == ingredient_in.ingredient_name,
    )
    if existing.first():
        raise ValueError(f"Ingredient '{ingredient_in.ingredient_name}' already exists.")

    ingredient = Ingredient(
        ingredient_name=ingredient_in.ingredient_name,
        estimated_shelf_life=ingredient_in.estimated_shelf_life,
        countability=ingredient_in.countability
    )
    ingredient.ingredienttags = db.query(IngredientTag).filter(
        IngredientTag.ingredient_tag_id.in_(ingredient_in.ingredienttag_ids)
    ).all()
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


"""
Retrieve the full list of ingredients from the database

Args:
    db (Session): database session

Returns:
    List[Ingredient]: full list of ingredients
"""
def get_ingredient_list(db: Session):
    return db.query(Ingredient).all()