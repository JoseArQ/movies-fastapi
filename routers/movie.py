from typing import Any, Dict, List

from fastapi import Query
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session

from models.movie import Movie as MovieModel

from schemas.movie import Movie
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get("/movies", tags=["movies"])
def get_movies() -> List[Movie]:
    db = Session()
    movies = MovieService(db=db).get_movies()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.get("/movies/{id}", tags=["movies"])
def get_movie(id : int):
   db = Session()
   movie_model = MovieService(db=db).get_movie(id=id)

   if not movie_model:
        return JSONResponse(status_code=404, content={
            "message": "record not found"
        })
   
   return JSONResponse(status_code=200, content=jsonable_encoder(movie_model))

@movie_router.get("/movies/", tags=["movies"]) # añadir / para que tome el queryparam
def get_movie_by_category(category : str = Query(min_length=3, max_length=20)): # los argumento son los query params
    db = Session()
    movies = MovieService(db=db).get_by_category(category=category)
    
    if not movies:
        return JSONResponse(status_code=404, content={
            "message": "record not found"
        })
    
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@movie_router.post("/movies", tags=["movies"], response_model=Movie, status_code=201)
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

@movie_router.put('/movies/{id}', tags=['movies'], status_code=200, response_model=dict)
def update_movie(id : int, movie : Dict[Any, Any]):
    db = Session()
    movie_record = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not movie_record:
        return JSONResponse(status_code=400, content={
            "message": "movie not found, invalid id"
        })
    
    print('movie: ', movie_record)
    movie_record.title = movie["title"]
    movie_record.overview = movie["overview"]
    movie_record.year = movie["year"]
    movie_record.rating = movie["rating"]
    movie_record.category = movie["category"]
    db.commit()
    return JSONResponse(status_code=200, content={
        "message": "movie update successfully"
    })    

@movie_router.delete('/movies/{id}', tags=['movies'], status_code=200)
def remove_movie(id : int):
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return JSONResponse(status_code=400, content={
            "message": "movie not found, invalid id"
        })
    
    db.delete(movie)
    db.commit()
    return JSONResponse(
        status_code=200,
        content={
            "message": "movie deleted succesfully!"
        }
    )