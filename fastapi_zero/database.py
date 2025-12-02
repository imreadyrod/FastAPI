from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

# Stablishing connection with db
engine = create_engine(Settings().DATABASE_URL)


# Open the path to db
def get_session():

    with Session(engine) as session:
        yield session
