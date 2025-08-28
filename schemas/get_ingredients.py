from pydantic import BaseModel
from typing import List


class ResponseSchema(BaseModel):
    ingredient_list: List[str]