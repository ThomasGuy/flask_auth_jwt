import os
import uuid
import datetime
import unittest
import click
import coverage
from pathlib import Path

from project.server import create_app
from project.server.bitfinex.bfx import bfx
from project.database import db_scoped_session as db, Base, init_db
from project.database.models import User, Blacklist

bfx.ws.run()
app, engine = create_app("config.DevelopmentConfig")


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Blacklist=Blacklist)

@app.cli.command()
def test():
    """Runs the unit test."""
    test = unittest.TestLoader().discover('project/test', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(test)
    if result.wasSuccessful():
        return 0
    return 1

@app.cli.command()
def drop():
    """ drops all database tables """
    print('Do you want to wipe the database? y/n...')
    response =  input()
    if response in ['y', 'yes']:
        db.remove()
        Base.metadata.drop_all(engine)
        print('\nDone')
    else:
        print('Start again...')

@app.cli.command()
def create_db():
    """ Creates the db tables if they don't already exist """
    init_db(app.config['SQLALCHEMY_DATABASE_URI'])
