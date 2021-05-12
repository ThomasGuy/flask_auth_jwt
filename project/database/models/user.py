''' User class '''
import datetime
import uuid

# third  party imports
from sqlalchemy import Column, String, Integer, Boolean, DateTime, or_

from .. import Base, flask_bcrypt


class User(Base):
    ''' User: <user> '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    public_id = Column(String(100), default=str(uuid.uuid4()))
    registered_on = Column(DateTime, default=datetime.datetime.utcnow())
    admin = Column(Boolean, nullable=False, default=False)
    password_hash = Column(String(100))

    @property
    def password(self):
        ''' password cannot be directly accessed '''
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        '''
        authenicate password
        :return: Boolean
        '''
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    @staticmethod
    def authenticate(password=None, username=None, email=None, public_id=None):
        '''
        Authenticate User
        :param password and one other
        :return: authenticated <user>|False
        '''
        found_user = User.query.filter(or_(
            User.username == username,
            User.email == email,
            User.public_id == public_id
        )).first()

        if found_user:
            if flask_bcrypt.check_password_hash(found_user.password_hash, password):
                return found_user
        return False

    def to_dict(self):
        '''
        User dictionary
        :return: dict
        '''
        return {
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'public_id': self.public_id
        }
