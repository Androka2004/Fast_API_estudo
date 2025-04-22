from dataclasses import asdict

from sqlalchemy import select

from api_rapidin_massa.models import Mano


def test_creador_suarrio(session, mock_db_time):
    with mock_db_time(model=Mano) as time:
        suarrio = Mano(
            username='Raios Funde', email='teste@mail.com', password='lombada'
        )

        session.add(suarrio)
        session.commit()

    resultado = session.scalar(
        select(Mano).where(Mano.email == 'teste@mail.com')
    )

    assert asdict(resultado) == {
        'id': 1,
        'username': 'Raios Funde',
        'password': 'lombada',
        'email': 'teste@mail.com',
        'created_at': time,
        'updated_at': time,
    }
