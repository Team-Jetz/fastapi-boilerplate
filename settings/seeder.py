from settings.hashing import Hash
from uuid import uuid4
from settings.databases import engine
from sqlalchemy import event

from app.account.models import User

INITIAL_DATA = {
      'users': [
            {
                'id': uuid4(),
                'username': 'admin',
                'email': 'superuser@example.com',
                'password': Hash.bcrypt('password@123')
            },
      ],
}

connection = engine.connect()

def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])

def initialize_data():
    event.listen(User.__table__, 'after_create', initialize_table)
