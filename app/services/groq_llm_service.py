import os 
import base64
import json
from typing import List, Optional

from groq import Groq
from dotenv import load_dotenv

from app.logging_config import logger
from app.schemas.create_recipe import Recipe
from app.schemas.get_ingredients import ResponseSchema as GetIngredientSchema
from app.utils import resize_image_bytes, log_func


class GroqClient():
    def __init__(
        self, 
        image_analize_model,
        text_generate_model,
        stream_mode
    ):  
        if image_analize_model is None:
            self.image_analize_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            self.image_analize_model = image_analize_model
        
        if text_generate_model is None:
            self.text_generate_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            self.text_generate_model = text_generate_model

        if stream_mode is None:
            self.stream_mode = False
        else: self.stream_mode = stream_mode
        
        self.prompts = {}
        
        load_dotenv()
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
        base64_str = base64.b64encode(image_bytes).decode("utf-8")
        base64_image = f"data:image/png;base64,{base64_str}"

        response = self.groq_client.chat.completions.create(
            model=self.image_analize_model,
            messages=[
                {"role": "system", "content": self.prompts["get_ingredients_system"]},
                {"role": "user", "content": [
                    {"type": "text", "text": self.prompts["get_ingredients_prompt"]},
                    {"type": "image_url", "image_url": {"url": base64_image}}
                ]}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "list_ingedients",
                    "schema": schema
                }
            },
            stream=self.stream_mode,
            stop=None
        )

        if not self.stream_mode:
            response_content = response.choices[0].message.content

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


        response = self.groq_client.chat.completions.create(
            model=self.text_generate_model,
            messages=[
                {"role": "system", "content": self.prompts["create_recipe_system"]},
                {
                    "role": "user",
                    "content": f"{self.prompts["create_recipe_prompt"]} \n\n Ingredients: {list_ingredients} \n Restrictions: {list_restrictions}"
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "list_ingedients",
                    "schema": schema
                }
            },
            stream=self.stream_mode,
            stop=None
        )

        if not self.stream_mode:
            response_content = response.choices[0].message.content

        return json.loads(response_content)   

        




