from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_rapidin_massa.models import Mano, table_registry


def test_creador_suarrio():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        suarrio = Mano(
            username='Raios Funde', email='teste@mail.com', password='lombada'
        )
        session.add(suarrio)
        session.commit()
        session.refresh(suarrio)

    assert suarrio.id == 1
