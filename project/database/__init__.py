""" database """

# 3rd party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt

db_scoped_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = db_scoped_session.query_property()
flask_bcrypt = Bcrypt()


def init_db(db_path):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import project.database.models
    engine = create_engine(db_path)
    db_scoped_session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    return engine
