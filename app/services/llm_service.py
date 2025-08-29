import os
import json
from typing import List, Optional

from ollama import Client
from dotenv import load_dotenv

from app.logging_config import logger
from app.schemas.create_recipe import Recipe
from app.schemas.get_ingredients import ResponseSchema as GetIngredientSchema



class LLMClient():
    def __init__(
            self, 
            image_analize_model="qwen2.5vl:7b",
            text_generate_model="qwen2.5vl:7b",
            stream_mode = False
    ):
        self.image_analize_model = image_analize_model
        self.text_generate_model = text_generate_model
        self.stream_mode = stream_mode
        self.prompts = {}

        load_dotenv()
        self.ollama_client = Client(host=os.getenv("OLLAMA_HOST"))


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


    def get_ingredients(self, image_bytes: str) -> dict:
        schema = GetIngredientSchema.model_json_schema()

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

        logger.info("responce_getted")
        return json.loads(response_content)


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
        else:
            response_content = ""
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    print(chunk["message"]["content"], end="", flush=True)
                    response_content += chunk["message"]["content"]

        logger.info("responce_getted")
        return json.loads(response_content)   