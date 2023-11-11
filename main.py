"""run application: uvicorn main:app --reload --port 5000"""

from typing import Any, Coroutine, Optional

from fastapi import FastAPI, Body, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from pydantic import BaseModel, Field
from starlette.requests import Request
from jwt_manager import create_token, validate_token

from config.database import Base, engine, Session
from models.movie import Movie as MovieModel

from schemas.movie import Movie
from schemas.user import User

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data['email'] != "admin@email.com":
            raise HTTPException(status_code=403, detail='credentials invalids')
    
    
app = FastAPI()

app.title = "My first FastApi application"
app.version = "0.0.1"

movies = [
    {
        "id": 1,
        "title": 'my movie',
        "category": "accion"
    },
    {
        "id": 2,
        "title": 'my movie 2',
        "category": "terror"
    },
]

def get_movie_by_id(id : int):
    for movie in movies:
        if movie["id"] == id:
            return movie


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

@app.get("/movies", tags=["movies"], dependencies=[Depends(JWTBearer())])
def get_movies():
    return JSONResponse(content=movies, status_code=200)

@app.get("/movies/{id}", tags=["movies"])
def get_movie(id : int):
    movie = get_movie_by_id(id=id)
    if movie:
        return {'data': movie}
    return {'data': None }

@app.get("/movies/", tags=["movies"]) # añadir / para que tome el queryparam
def get_movie_by_category(category : str): # los argumento son los query params

    for movie in movies:
        if movie['category'].lower() == category.lower():
            return {'data': movie}
    return {'data': None}

@app.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie : Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(
        content={"message": "movie register succesfully"},
        status_code=201
    )

@app.put('/movies/{id}', tags=['movies'])
def update_movie(movie : Movie):

    for movie in movies:
        if movie["id"] == id:
            movie['title'] = movie.title
            movie['category'] = movie.category
            return {'data':movies}

    return {'data': None}    
