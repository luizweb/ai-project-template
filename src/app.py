from http import HTTPStatus

from fastapi import FastAPI

from src.schemas import Message

app = FastAPI()


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
async def root():
    return {"message": "FastAPI is running!"}
