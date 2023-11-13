from typing import List
from models.movie import Movie

class MovieService:

    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        return self.db.query(Movie).all()
    
    def get_movie(self, id : int) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.id == id).first()
    
    def get_by_category(self, category : str) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.category == category).all()