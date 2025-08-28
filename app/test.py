import json

from utils import resize_image_bytes
from services import llm_service


with open("images/ggg.jpeg", "rb") as f:
    image_bytes = f.read()


clien = llm_service.LLMClient()
ingr = clien.get_ingredients(resize_image_bytes(image_bytes))
print(json.dumps(ingr, indent=4), end="\n\n\n")

recipe = clien.create_resipe(list_ingredients=ingr["ingredient_list"])
print(json.dumps(recipe, indent=4))





