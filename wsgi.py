"""
development config
flask shell
flask test
flask drop
flask create_db
flask prune_db
"""

import unittest

from flask.cli import with_appcontext

from project.database import Base, init_db
from project.database import db_scoped_session as db
from project.database.models import Blocklist, User
from project.server import create_app
from project.server.bitfinex.bfx import bfx
from project.server.util.blacklist_helpers import prune_database

# from project.server.services.events import sockio

app, engine = create_app('config.DevelopmentConfig')


@app.cli.command('start')
@with_appcontext
def start():
    """start application in development mode"""
    bfx.ws.run()


@app.shell_context_processor
def make_shell_context():
    """
    Can add a user to db:-
    user = User(username= ..., ...)
    db.add(user)
    db.commit()
    """
    return dict(app=app, db=db, User=User, Blocklist=Blocklist)


@app.cli.command()
@with_appcontext
def test():
    """Runs the unit test."""
    bfx.ws.run()
    atest = unittest.TestLoader().discover('project/test', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(atest)
    if result.wasSuccessful():
        # stop_bfx()
        return 0
    # bfx.ws.unsubscribe_all()
    return 1


@app.cli.command()
def drop():
    """drops all database tables"""
    print('Do you want to wipe the database? y/n...')
    response = input()
    if response in ['y', 'yes']:
        db.remove()
        Base.metadata.drop_all(engine)
        print('\nDone')
    else:
        print('Start again...')


@app.cli.command('create_db')
def create_db():
    """Creates the db tables if they don't already exist"""
    init_db(app.config['SQLALCHEMY_DATABASE_URI'])


@app.cli.command('prune_db')
def prune_db():
    """Remove all expired tokens from Blocklist db"""
    prune_database()


# if __name__ == "__main__":
#     bfx.ws.run()
#     sockio.run(app, host='localhost', port=7000)
