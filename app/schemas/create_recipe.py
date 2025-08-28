from pydantic import BaseModel
from typing import List
from datetime import datetime

class Step(BaseModel):
    step_number: int
    action: str


class RecipeIngredient(BaseModel):
    name: str
    count_gram: int


class Recipe(BaseModel):
    title: str
    ingredients: List[RecipeIngredient]
    steps: List[Step]
    list_restrictions: List[str]
    calories: int
    weidth_grams: int
    time_to_cook_minutes: int 
