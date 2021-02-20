import requests
import json
from datetime import timedelta

from decorators import connection_exceptions
from app import r


class Stock():

    PAIRS_API_URL: str

    raw_pairs: list = []
    pairs: list = []
    # Format of values in pairs must be: 
    # [
    #       'BTC/ETH', - like human readble(with slash)
    # ]
    
    def __init__(self):
        self.get_pairs()
        

    @connection_exceptions()
    def get_raw_pairs(self, url) -> list:
        return requests.get(url)


    def get_pairs(self):
        if r.exists(self.REDIS_PAIRS_KEY):
            return json.loads(r.get(self.REDIS_PAIRS_KEY))
        else:
            self.raw_pairs = self.get_raw_pairs(self.PAIRS_API_URL).json()
            self.pairs = self.parse_pairs()
            r.setex(
                self.REDIS_PAIRS_KEY,
                timedelta(days=1),
                value=json.dumps(self.pairs)
            )
            return self.pairs


class Kraken(Stock):

    PAIRS_API_URL = 'https://api.kraken.com/0/public/AssetPairs'
    REDIS_PAIRS_KEY = 'kraken_pairs_list'


    def parse_pairs(self):
        return [x['wsname'] for x in self.raw_pairs['result'].values() if 'wsname' in x]


class Binance(Stock):

    PAIRS_API_URL = 'https://api3.binance.com/api/v3/exchangeInfo'
    REDIS_PAIRS_KEY = 'binance_pairs_list'


    def parse_pairs(self):
        return list(map(lambda x: f"{x['baseAsset']}/{x['quoteAsset']}", self.raw_pairs['symbols']))
