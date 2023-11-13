from typing import List, Dict, Any
from models.movie import Movie

class MovieService:

    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self)-> List[Movie]:
        return self.db.query(Movie).all()
    
    def get_movie(self, id : int) -> Movie:
        return self.db.query(Movie).filter(Movie.id == id).first()
    
    def get_by_category(self, category : str) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.category == category).all()
    
    def create(self, movie_data : Dict[Any, Any]) -> None:
        new_movie = Movie(**movie_data)
        self.db.add(new_movie)
        self.db.commit()
        return None
    
    def update(self, id : int, movie_data : Dict[Any, Any]) -> None:
        movie = self.db.query(Movie).filter(Movie.id == id).first()
        movie.title = movie_data['title']
        movie.overview = movie_data['overview']
        movie.rating = movie_data['rating']
        movie.year = movie_data['year']
        movie.category = movie_data['category']
        self.db.commit()
        return None
    
    def delete(self, id : int) -> None:
        movie = self.db.query(Movie).filter(Movie.id == id).delete()
        self.db.commit()
        return None