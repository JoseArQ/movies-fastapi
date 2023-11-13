from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token

from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user : User) -> User:
    token : str = ''
    if user.email == "admin@email.com" and user.password == "admin":
        token  = create_token(data=user.dict())
    return JSONResponse(content=token, status_code=200)