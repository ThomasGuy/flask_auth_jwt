"""
initialize and open Bitfinex websocket
"""

import logging
import os

# 3rd party imports
from bfxapi import Client

# package imports
from project.server.services.events import sockio

from .Vault import Ticker

log = logging.getLogger(__name__)
API_KEY = os.getenv('BFX_KEY')
API_SECRET = os.getenv('BFX_SECRET')

symlong = [
    'BTC',
    'BSV',
    'BTG',
    'DSH',
    'EOS',
    'ETC',
    'ETH',
    'ETP',
    'IOT',
    'LTC',
    'NEO',
    'OMG',
    'SAN',
    'TRX',
    'XLM',
    'XMR',
    'XRP',
    'XTZ',
    'ZEC',
    'ZRX',
]

sym2 = ['BTC', 'ETH', 'XRP', 'LTC', 'NEO', 'BSV', 'EOS', 'ETC', 'XMR', 'XTZ']
symsmall = ['BTC', 'ETH', 'XRP', 'LTC']

tickerDataFields = [
    'daily_change',
    'daily_change_relative',
    'last_price',
    'volume',
    'high',
    'low',
]

vault = {}

bfx = Client(
    # API_KEY=API_KEY,
    # API_SECRET=API_SECRET,
    logLevel='INFO',
    channel_filter=['ticker', 'candle'],
)


@bfx.ws.on('error')  # type: ignore
def log_error(message):
    """
    log error message
    """
    log.error(message)


@bfx.ws.on('subscribed')  # type: ignore
def show_A_channel(sub):
    """
    subscrbed ticker add it to vault
    """
    symbol = sub.symbol[1:]
    vault[symbol] = Ticker(symbol=symbol)
    log.info(f'{symbol} subscribed - added to vault, size = {len(vault)}')


@bfx.ws.on('all')  # type: ignore
def bfxws_data_handler(data):
    """
    emit ticker updates from bitfinex to all
    """
    if isinstance(data, str):
        log.info(f'bfx-info: {data}')


@bfx.ws.on('new_ticker')  # type: ignore
def new_ticker_update(data):
    """
    a new ticker update has benn issued
    """
    symbol = str(data.pair[1:])
    update = {
        'daily_change': data.daily_change,
        'daily_change_rel': data.daily_change_rel,
        'last_price': data.last_price,
        'volume': data.volume,
        'high': data.high,
        'low': data.low,
    }

    vault[symbol].update(**update)
    sockio.emit(
        'ticker_update',
        {'data': vault[symbol].as_dict()},
        namespace='/api',
        broadcast=True,
    )


async def start():
    """
    start bitfinex api websocket
    """
    await bfx.ws.subscribe('ticker', 'tBTCUSD')
    for sym in symlong[1:]:
        # btc = f't{sym}BTC'
        usd = f't{sym}USD'
        await bfx.ws.subscribe('ticker', usd)
        # await bfx.ws.subscribe('ticker', btc)


async def stop_bfx():
    """stop the web socket nicely"""
    await bfx.ws.unsubscribe_all()
    await bfx.ws.stop()


bfx.ws.on('connected', start)
