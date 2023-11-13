"""run application: uvicorn main:app --reload --port 5000"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from config.database import Base, engine

from middlewares.error_handler import ErrorHandlrer
from middlewares.jwt_bearer import JWTBearer

from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()

app.title = "My first FastApi application"
app.version = "0.0.1"

app.add_middleware(ErrorHandlrer)

app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

  
@app.get("/", tags=["home"])
async def root():
    return HTMLResponse(
        content="<h1>HELLO WORLD!</h1>"
    )