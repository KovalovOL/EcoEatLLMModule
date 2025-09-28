from typing import List
from fastapi import FastAPI, Query, File, UploadFile

from app.factories.llm_factory import LLMFactory


app = FastAPI(root_path="/llm")
llmFactory = LLMFactory()
client = LLMFactory.create_client(client_name="groq")


@app.get("/")
async def ping():
    return {"message": "pong"}


@app.post("/get_ingredients")
async def get_ingredients(file: UploadFile = File(...)) -> dict:
    image_bytes = await file.read()
    return client.get_ingredients(image_bytes)


@app.get("/create_resipe")
async def create_resipe(
    list_ingredients: List[str] = Query(...),
    list_restrictions: List[str] = Query([])
) -> dict:
    return client.create_recipe(
        list_ingredients=list_ingredients,
        list_restrictions=list_restrictions
    )