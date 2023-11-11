from pydantic import BaseModel, Field

class User(BaseModel):
    email : str
    password : str
