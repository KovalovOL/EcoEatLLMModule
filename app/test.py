import json
import os

from app.utils import resize_image_bytes
from app.services import llm_service


base_dir = os.path.dirname(__file__)
image_folder_path = os.path.join(base_dir, "images")
image_folder_path = os.path.abspath(image_folder_path)
        

with open(f"{image_folder_path}/ggg.jpeg", "rb") as f:
    image_bytes = f.read()


clien = llm_service.LLMClient()
ingr = clien.get_ingredients(resize_image_bytes(image_bytes))
print(json.dumps(ingr, indent=4), end="\n\n\n")

recipe = clien.create_resipe(list_ingredients=ingr["ingredient_list"])
print(json.dumps(recipe, indent=4))





