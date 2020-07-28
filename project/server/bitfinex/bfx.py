'''
    initialize and open Bitfinex websocket
'''
import logging
import os
import json
import asyncio

# 3rd party imports
from bfxapi import Client

# package imports
from project.server.services.events import sockio
from .Vault import Ticker, TickerBank


log = logging.getLogger(__name__)
API_KEY = os.getenv('BFX_KEY')
API_SECRET = os.getenv('BFX_SECRET')

symbols = ['BTC', 'BCH', 'BSV', 'BTG', 'DSH', 'EOS', 'ETC', 'ETH', 'ETP', 'IOT',
           'LTC', 'NEO', 'OMG', 'SAN', 'TRX', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZRX']

sym2 = ['BTC', 'ETH', 'XRP', 'LTC', 'NEO', 'BSV', 'EOS', 'ETC', 'XMR', 'XTZ']
small = ['BTC', 'ETH', 'XRP', 'LTC']
tickerDataFields = ['daily_change', 'daily_change_relative', 'last_price',
                    'volume', 'high', 'low']

# vault = TickerBank()  # Ticker dataclass instamces in the TickerBank vault
vault = {}


bfx = Client(
    # API_KEY=API_KEY,
    # API_SECRET=API_SECRET,
    logLevel='INFO',
    dead_man_switch=True,
    channel_filter=['ticker', 'candle'],
    )

@bfx.ws.on('error')
def log_error(message):
    log.error(message)


@bfx.ws.on('subscribed')
def show_channel(sub):
    symbol = sub.symbol[1:]
    vault[symbol] = Ticker(symbol=symbol)
    log.info(f"{symbol} subscribed - added to vault, size = {len(vault)}")


@bfx.ws.on('all')
def bfxws_data_handler(data):
    if type(data) is list:
        dataEvent = data[1]
        chan_id = data[0]

        if type(dataEvent) is not str and bfx.ws.subscriptionManager.is_subscribed(chan_id):
            sub = bfx.ws.subscriptionManager.get(chan_id)
            if sub.channel_name == 'ticker':
                update = dict(zip(tickerDataFields, dataEvent[4:]))
                vault[sub.symbol[1:]]._update(**update)

                update['symbol'] = sub.symbol[1:]

                payload = {
                    'data': update,
                    }
                sockio.emit('ticker_update', json.dumps(update), namespace='/api', broadcast=True)
                # log.debug(f'{sub.symbol} - ticker event')
    else:
        log.info(f'bfx-info: {data}')

async def start():
    await bfx.ws.subscribe('ticker', 'tBTCUSD')
    for sym in sym2[1:]:
        # btc = f't{sym}BTC'
        usd = f't{sym}USD'
        await bfx.ws.subscribe('ticker', usd)
        # await bfx.ws.subscribe('ticker', btc)

bfx.ws.on('connected', start)
