from typing import Optional, Union
from pydantic import BaseModel, Field

class Movie(BaseModel):
    int : Optional[int] = None
    title : str 
    overview : str 
    year : int 
    rating : Union[int, float] 
    category : str 