from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from enums.countability import Countability
from core.database import Base

ingredient_ingredienttag = Table(
    'ingredient_ingredienttag', Base.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredient.ingredient_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('ingredient_tag.tag_id'), primary_key=True)
)

class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False, unique=True)
    estimated_shelf_life = Column(Integer, nullable=True)
    countability = Column(Enum(Countability), nullable=False)

    ingredienttags = relationship("IngredientTag", secondary=ingredient_ingredienttag, back_populates="ingredients")

    @property
    def ingredienttag_ids(self):
        return [tag.ingredient_tag_id for tag in self.ingredienttags]

class IngredientTag(Base):
    __tablename__ = "ingredient_tag"

    ingredient_tag_id = Column(Integer, primary_key=True)
    ingredient_tag_name = Column(String, nullable=False, unique=True)

    ingredients = relationship("Ingredient", secondary=ingredient_ingredienttag, back_populates="ingredienttags")

