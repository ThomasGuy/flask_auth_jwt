"""Data holder"""

import collections
from dataclasses import asdict, dataclass


@dataclass
class Ticker:
    """Store ticker data in instance of Ticker dataclass"""

    symbol: str
    daily_change: float = -0.01
    daily_change_rel: float = -0.01
    last_price: float = -0.01  # latest ticker
    volume: float = -0.01
    high: float = -0.01
    low: float = -0.01

    def update(self, **kwargs):
        """update Ticker from dict"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def as_dict(self):
        """return as dictionary"""
        return asdict(self)


class TickerBank(collections.UserList):
    """Contains all Ticker instances"""

    def getTicker(self, symbol):
        """Return Ticker instance"""
        for ticker in self:
            if symbol in ticker.symbol:
                return ticker
        return None


class TickerDict(collections.UserDict):
    """Dictionary of ticker objects
    key: symbol
    value: Ticker - dataclass
    """

    def getAll(self):
        """return all tickers"""
        return self.values()

    def getList(self, symbols):
        """return selected tickers"""
        tickers = []

        for sym in symbols:
            try:
                tickers.append(self[sym])
            except KeyError:
                tickers.append(f'Error {sym}: No such {sym}')
        return tickers
