from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from src.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

# Teste de lista como database
database = []


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
async def root():
    return {'message': 'FastAPI is running!'}


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # .model_dump() é um método de modelos do pydantic
    # que converte o objeto em dicionário.

    # Os ** querem dizer que o dicionário será desempacotado em parâmetros.
    # Fazendo com que a chamada seja equivalente a
    # UserDB(username='nome do usuário', password='senha do usuário',
    # email='email do usuário', id=len(database) + 1)
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
