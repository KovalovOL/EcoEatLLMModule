import os
import json
from typing import List, Optional

from ollama import Client
from dotenv import load_dotenv

from app.logging_config import logger
from app.schemas.create_recipe import Recipe
from app.schemas.get_ingredients import ResponseSchema as GetIngredientSchema
from app.utils import resize_image_bytes, log_func


class LocalOllamaClient():
    def __init__(
        self, 
        image_analize_model,
        text_generate_model,
        stream_mode
    ):
        if image_analize_model is None:
            self.image_analize_model = "qwen2.5vl:7b"
        else:
            self.image_analize_model = image_analize_model
        
        if text_generate_model is None:
            self.text_generate_model = "qwen2.5vl:7b"
        else:
            self.text_generate_model = text_generate_model

        if stream_mode is None:
            self.stream_mode = False
        else: self.stream_mode = stream_mode
        
        self.prompts = {}

        load_dotenv()
        self.ollama_client = Client(host=os.getenv("OLLAMA_HOST"))

        #Load all prompts
        base_dir = os.path.dirname(__file__)
        prompts_folder_path = os.path.join(base_dir, "..", "prompts")
        prompts_folder_path = os.path.abspath(prompts_folder_path)

        for prompt_file_name in os.listdir(prompts_folder_path):
            prompt_file_path = os.path.join(prompts_folder_path, prompt_file_name)
            if os.path.isfile(prompt_file_path):
                key = prompt_file_name.split(".")[0]
                with open(prompt_file_path, "r") as f:
                    self.prompts[key] = f.read()
        logger.info("prompts_loaded")
        logger.info("llm_client_created")


    @log_func
    def get_ingredients(self, image_bytes: str) -> dict:
        schema = GetIngredientSchema.model_json_schema()
        image_bytes = resize_image_bytes(image_bytes)


        response = self.ollama_client.chat(
            model=self.image_analize_model,
            messages=[
                {"role": "system", "content": self.prompts["get_ingredients_system"]},
                {"role": "user", "content": self.prompts["get_ingredients_prompt"], "images": [image_bytes]}
            ],
            format=schema,
            stream=self.stream_mode
        )

        if not self.stream_mode:
            response_content = response.message.content
        else:
            response_content = ""
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    print(chunk["message"]["content"], end="", flush=True)
                    response_content += chunk["message"]["content"]

        return json.loads(response_content)


    @log_func
    def create_recipe(
            self,
            list_ingredients: List[str],
            list_restrictions: Optional[List[str]] = None
    ) -> str:
        if list_restrictions is None:
            list_restrictions = []

        schema = Recipe.model_json_schema()
        response = self.ollama_client.chat(
            model=self.image_analize_model,
            messages=[
                {"role": "system", "content": self.prompts["create_recipe_system"]},
                {
                    "role": "user",
                    "content": f"{self.prompts["create_recipe_prompt"]} \n\n Ingredients: {list_ingredients} \n Restrictions: {list_restrictions}"
                }
            ],
            format=schema,
            stream=self.stream_mode
        )

        if not self.stream_mode:
            response_content = response.message.content

        return json.loads(response_content)   