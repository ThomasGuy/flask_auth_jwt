import datetime

# third  party imports
from sqlalchemy import Column, String, Integer, Boolean, DateTime, or_

from .. import Base, flask_bcrypt
from . import Blacklist


class User(Base):
    ''' User: <user> '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    public_id = Column(String(100), unique=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    # using class method here since we will be invoking this using User.authenticate()
    @staticmethod
    def authenticate(password, username=None, email= None, public_id=None):
        found_user = User.query.filter(or_(
                User.username==username,
                User.email==email,
                User.public_id==public_id
            )).first()

        if found_user:
            if flask_bcrypt.check_password_hash(found_user.password_hash, password):
                return found_user # make sure to return the user so we can log them in by storing information in the session
        return False

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'public_id': self.public_id
        }
