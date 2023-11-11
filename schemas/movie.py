from typing import Optional, Union
from pydantic import BaseModel, Field

class Movie(BaseModel):
    int : Optional[int] = None
    title : str = Field(..., max_length=100)
    overview : str = Field(..., max_length=500)
    year : int = Field(..., gt=1900, le=2023)
    rating : Union[int, float] = Field(..., gt=0.0, lt=10.0)
    category : str = Field(..., max_length=100)