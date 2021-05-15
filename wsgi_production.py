""" launch production server """

from project.server import create_app
from project.server.bitfinex.bfx import bfx


app, engine = create_app("config.ProductionConfig")
bfx.ws.run()
