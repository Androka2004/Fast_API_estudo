from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_rapidin_massa.settings import Configis

engine = create_engine(Configis().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
