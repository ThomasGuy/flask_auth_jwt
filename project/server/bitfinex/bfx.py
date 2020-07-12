'''
    initialize and open Bitfinex websocket
'''
import logging
import os
import json

# 3rd party imports
from bfxapi import Client

# package imports
# from server.events import sockio
from .Vault import Ticker, TickerBank


log = logging.getLogger(__name__)
API_KEY = os.getenv('BFX_KEY')
API_SECRET = os.getenv('BFX_SECRET')

symbols = ['BTC', 'BCH', 'BSV', 'BTG', 'DSH', 'EOS', 'ETC', 'ETH', 'ETP', 'IOT',
           'LTC', 'NEO', 'OMG', 'SAN', 'TRX', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZRX']

sym2 = ['BTC', 'ETH', 'XRP', 'LTC', 'NEO', 'BSV', 'EOS', 'ETC']
small = ['BTC', 'ETH', 'XRP', 'LTC']
tickerDataFields = ['daily_change', 'daily_change_percent', 'last_price',
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
def log_error(msg):
    log.error(msg)


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
                updates = dict(zip(tickerDataFields, dataEvent[4:]))
                vault[sub.symbol[1:]]._update(**updates)

                # payload = {
                #     'symbol': sub.symbol[1:],
                #     'data': dataEvent[4:],
                #     }
                # sockio.emit('ticker event', json.dumps(payload), namespace='/main', broadcast=True)
                log.debug(f'{sub.symbol} - ticker event')
    else:
        log.info(f'bfx-info: {data}')

# @bfx.ws.on ('new_ticker')
# def update_ticker(data):
#     log.info(f'tick_update: {data}')
    #            tick_update: Ticker 'tETHUSD' <last='173.63029311' volume=55517.73711568>

async def start():
    await bfx.ws.subscribe('ticker', 'tBTCUSD')
    for sym in sym2[1:]:
        # btc = f't{sym}BTC'
        usd = f't{sym}USD'
        await bfx.ws.subscribe('ticker', usd)
        # await bfx.ws.subscribe('ticker', btc)

bfx.ws.on('connected', start)
