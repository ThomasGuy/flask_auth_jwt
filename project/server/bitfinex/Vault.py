''' Data holder '''
from dataclasses import dataclass


@dataclass
class Ticker():
    '''Store ticker data in instance of Ticker dataclass'''
    symbol: str
    daily_change: float = -0.01
    daily_change_relative: float = -0.01
    last_price: float = -0.01   # latest ticker
    volume: float = -0.01
    high: float = -0.01
    low: float = -0.01

    def update(self, **kwargs):
        """ update Ticker from dict """
        for key, value in kwargs.items():
            setattr(self, key, value)


class TickerBank(list):
    ''' Contains all Ticker instances '''

    def getTicker(self, symbol):
        '''Return Ticker instance'''
        for ticker in self:
            if symbol in ticker.symbol:
                return ticker
        return None


class TickerDict(dict):
    ''' Dictionary of ticker objects
        key: symbol
        value: Ticker - dataclass
    '''
    pass
