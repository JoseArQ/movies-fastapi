import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_name = "movies"
user = "josep"
password = "admin123"
host = "localhost"

database_url = f"postgresql://{user}:{password}@{host}/{db_name}"

# base_dir = os.path(os.path.dirname(os.path.realpath(__file__)))

engine = create_engine(url=database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()