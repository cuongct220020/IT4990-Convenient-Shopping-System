from typing import List
import httpx
from sqlalchemy.orm import Session
from models.recipe import Recipe, RecipeCountableIngredient, RecipeUncountableIngredient
from schemas.recipe_schema import RecipeIn, RecipeOut, CountableIngredient, UncountableIngredient

"""
2 steps:
1. Call Ingredient Service to get all ingredient names and map them by their IDs.
2. Fetch all recipes from the database and replace ingredient IDs with names using the mapping from step 1.
Using async for lower coupling
"""

INGREDIENT_SERVICE_URL = "http://127.0.0.1:8000/ingredients/"

async def fetch_ingredient_data() -> dict[int, dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(INGREDIENT_SERVICE_URL)
        response.raise_for_status()
        ingredients = response.json()
    return {
        int(ingredient['ingredient_id']): {
            'ingredient_name': ingredient['ingredient_name'],
            'countability': ingredient['countability']
        }
        for ingredient in ingredients
    }

async def get_all_recipes(db: Session) -> List[RecipeOut]:
    result = db.execute(Recipe.__table__.select())
    recipes = result.scalars().all()

    ingredient_data = await fetch_ingredient_data()

    output: List[RecipeOut] = []
    for recipe in recipes:
        countable_ingredients = [
            CountableIngredient(
                ingredient_id=ci.ingredient_id,
                ingredient_name=ingredient_data.get(ci.ingredient_id, {}).get("ingredient_name", "Unknown"),
                quantity=ci.quantity
            )
            for ci in recipe.countable_ingredients
        ]
        uncountable_ingredients = [
            UncountableIngredient(
                ingredient_id=ui.ingredient_id,
                ingredient_name=ingredient_data.get(ui.ingredient_id, {}).get("ingredient_name", "Unknown"),
                quantity=ui.quantity,
                unit=ui.unit.value
            )
            for ui in recipe.uncountable_ingredients
        ]
        output.append(RecipeOut(
            recipe_id=recipe.recipe_id,
            recipe_name=recipe.recipe_name,
            default_servings=recipe.default_servings,
            instructions=recipe.instructions,
            countable_ingredients=countable_ingredients,
            uncountable_ingredients=uncountable_ingredients
        ))
    return output

async def create_recipe(db: Session, recipe_in: RecipeIn) -> RecipeOut:
    ingredient_data = await fetch_ingredient_data()

    for ci in recipe_in.countable_ingredients:
        data = ingredient_data.get(ci.ingredient_id, {})
        if not data:
            raise ValueError(f"Countable ingredient ID {ci.ingredient_id} does not exist.")
        if data["countability"] != "countable":
            raise ValueError(f"Ingredient ID {ci.ingredient_id} is uncountable.")

    for ui in recipe_in.uncountable_ingredients:
        data = ingredient_data.get(ui.ingredient_id, {})
        if not data:
            raise ValueError(f"Uncountable ingredient ID {ui.ingredient_id} does not exist.")
        if data["countability"] != "uncountable":
            raise ValueError(f"Ingredient ID {ui.ingredient_id} is countable.")

    recipe = Recipe(
        recipe_name=recipe_in.recipe_name,
        default_servings=recipe_in.default_servings,
        instructions=recipe_in.instructions
    )
    recipe.countable_ingredients = [
        RecipeCountableIngredient(
            ingredient_id=ci.ingredient_id,
            quantity=ci.quantity
        )
        for ci in recipe_in.countable_ingredients
    ]
    recipe.uncountable_ingredients = [
        RecipeUncountableIngredient(
            ingredient_id=ui.ingredient_id,
            quantity=ui.quantity,
            unit=ui.unit
        )
        for ui in recipe_in.uncountable_ingredients
    ]
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return RecipeOut(
        recipe_id=recipe.recipe_id,
        recipe_name=recipe.recipe_name,
        default_servings=recipe.default_servings,
        instructions=recipe.instructions,
        countable_ingredients=recipe.countable_ingredient_list,
        uncountable_ingredients=recipe.uncountable_ingredient_list
    )


