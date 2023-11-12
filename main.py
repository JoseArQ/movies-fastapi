"""run application: uvicorn main:app --reload --port 5000"""

from typing import Any, Dict, Coroutine, Optional

from fastapi import FastAPI, Body, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder

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


def get_movie_by_id(id : int):
    movies = None
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

@app.get("/movies", tags=["movies"])
def get_movies():
    db = Session()
    movies = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@app.get("/movies/{id}", tags=["movies"])
def get_movie(id : int):
   db = Session()
   movie_model = db.query(MovieModel).filter(MovieModel.id == id).first()

   if not movie_model:
        return JSONResponse(status_code=404, content={
            "message": "record not found"
        })
   
   return JSONResponse(status_code=200, content=jsonable_encoder(movie_model))

@app.get("/movies/", tags=["movies"]) # añadir / para que tome el queryparam
def get_movie_by_category(category : str = Query(min_length=3, max_length=20)): # los argumento son los query params
    db = Session()
    movies = db.query(MovieModel).filter(MovieModel.category == category).all()
    
    if not movies:
        return JSONResponse(status_code=404, content={
            "message": "record not found"
        })
    
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@app.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
def create_movie(movie : Dict[Any, Any]) -> dict:
    # print('create a new movie')
    # print(f'input movie: {movie}')

    db = Session()
    new_movie = MovieModel(**movie)
    db.add(new_movie)
    db.commit()
    return JSONResponse(
        content={
            "movie": movie,
            "message": "movie register succesfully"
            },
        status_code=201
    )

@app.put('/movies/{id}', tags=['movies'], status_code=200, response_model=dict)
def update_movie(id : int, movie : Movie):
    movies = None
    for movie in movies:
        if movie["id"] == id:
            movie['title'] = movie.title
            movie['category'] = movie.category
            return {'data':movies}

    return {'data': None}    
