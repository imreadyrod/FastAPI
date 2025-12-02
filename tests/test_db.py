from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):

    # Every test will happen at mock_db_time.
    # This ensure that we can setup the time that the event happen
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)  # Add data into bd

        session.commit()  # ensuring that the operation happened

        # get the new_user. What came from db was converted into python object
        user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
    }
