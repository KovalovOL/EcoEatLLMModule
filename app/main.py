from fastapi import FastAPI
from services import llm_service


app = FastAPI()
client = llm_service.LLMClient()


@app.get("/")
async def ping():
    return {"message": "pong"}


@app.get("/get_ingredients")
async def get_ingredients(image_bytes: str) -> dict:
    return client.get_ingredients(image_bytes)


@app.get("/create_resipe")
async def create_resipe(
    list_ingredients: list,
    list_restrictions: list
) -> dict:
    return client.create_resipe(
        list_ingredients=list_ingredients,
        list_restrictions=list_restrictions
    )