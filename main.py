"""run application: uvicorn main:app --reload --port 5000"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from jwt_manager import create_token

from config.database import Base, engine

from middlewares.error_handler import ErrorHandlrer
from middlewares.jwt_bearer import JWTBearer

from routers.movie import movie_router

from schemas.user import User
    
app = FastAPI()

app.title = "My first FastApi application"
app.version = "0.0.1"

app.add_middleware(ErrorHandlrer)

app.include_router(movie_router)

Base.metadata.create_all(bind=engine)

@app.post('/login', tags=['auth'])
def login(user : User) -> User:
    token : str = ''
    if user.email == "admin@email.com" and user.password == "admin":
        token  = create_token(data=user.dict())
    return JSONResponse(content=token, status_code=200)
  
@app.get("/", tags=["home"])
async def root():
    return HTMLResponse(
        content="<h1>HELLO WORLD!</h1>"
    )