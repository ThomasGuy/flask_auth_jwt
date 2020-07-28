from project.server import create_app
from project.server.bitfinex.bfx import bfx

import asyncio

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
app, engine = create_app("config.ProductionConfig")
bfx.ws.run()
