from pydantic import BaseModel, Field, validators
from typing import List, Optional

# Define schema corresponds to database payload, base on Pydantic
class CountableIngredient(BaseModel):
    ingredient_name: str = Field(..., description="Tên nguyên liệu có thể đếm được theo số lượng (ví dụ: 2 quả trứng, 3 củ hành).")
    quantity: Optional[float] = Field(None, description="Số lượng nguyên liệu, dạng số.")
    unit: Optional[str] = Field(None, description="Đơn vị đếm rời rạc, ví dụ: quả, củ, bó, con, cái.")

class UncountableIngredient(BaseModel):
    ingredient_name: str = Field(..., description="Tên nguyên liệu không thể đếm theo đơn vị quả/cái mà thường theo khối lượng hoặc thể tích (ví dụ: 500g cá, 1 muỗng canh nước mắm).")
    quantity: Optional[float] = Field(None, description="Giá trị số lượng của nguyên liệu.")
    unit: Optional[str] = Field(None, description="Đơn vị đo lường, ví dụ: g, kg, muỗng canh, lít.")

class Recipe(BaseModel):
    recipe_name: str = Field(..., description="Tên món ăn.")
    default_servings: Optional[int] = Field(
        None,
        description="Số người ăn mà công thức này được thiết kế cho."
    )
    instructions: str = Field(..., description="Phần mô tả cách nấu món ăn.")
    countable_ingredients: List[CountableIngredient] = Field(
        ..., description="Danh sách các nguyên liệu có thể đếm được."
    )
    uncountable_ingredients: List[UncountableIngredient] = Field(
        ..., description="Danh sách các nguyên liệu không thể đếm, thường có đơn vị đo."
    )
