import os
import redis
import json
import logging

from time import sleep
from binance.client import Client
from binance.websockets import BinanceSocketManager
from schema import parse_data

logging.basicConfig(level=logging.INFO)
logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

r = redis.StrictRedis(
    host=os.environ.get('REDIS_URL'),
    port=6379,
    db=0,
    password=os.environ.get('REDIS_PASSWORD', None))


class Binance():

    def __init__(self):
        # self.pubsub = pubsub
        self.stock_name = 'binance'
        self.data = {}
        self.client = Client()
        self.ex_info = self.client.get_exchange_info()
        self.raw_pairs = dict(map(lambda x: (x['symbol'], x['baseAsset']), self.ex_info['symbols']))
        self.pairs = dict(map(lambda x: (x[0], f"{x[1]}/{x[0].replace(x[1], '')}"), self.raw_pairs.items()))
        self.get_price()
        self.subscription()


    def get_price(self):
        result = {'binance': {}}
        prices = self.client.get_all_tickers()
        [result['binance'].update({self.pairs[item['symbol']]: item['price']}) for item in prices]
        r.publish('tickers', json.dumps(result, indent=' '))


    def process_message(self, msg):
        if isinstance(msg, list):
            self.data = parse_data(msg, self.pairs)
            r.publish('tickers', json.dumps({self.stock_name: self.data}, indent=' '))


    def subscription(self):
        self.ws = BinanceSocketManager(self.client)
        self.ws.start_ticker_socket(self.process_message)
        self.ws.start()


if __name__=="__main__":
    Binance()