import os
import json
import requests
import json
import redis
import logging

from time import sleep
from kraken_wsclient_py import kraken_wsclient_py as KrakenClient


logging.basicConfig(level=logging.DEBUG)
logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

r = redis.StrictRedis(
    host=os.environ.get('REDIS_URL'),
    port=6379,
    db=0,
    password=os.environ.get('REDIS_PASSWORD', None))


class Kraken():

    def __init__(self):
        self.stock_name = 'kraken'
        self.data = {}
        self.ws = KrakenClient.WssClient()
        self.pairs_name_map = self.get_pairs()
        # self.get_price()
        self.subscription()


    def get_pairs(self) -> list:
        response = requests.get('https://api.kraken.com/0/public/AssetPairs')
        return dict({(name, value['wsname']) for name, value in response.json()['result'].items() if value.get('wsname')})


    def get_price(self):
        # payload = ','.join(self.get_pairs())
        # logging.info(payload)
        defect = []
        pairs = list(self.pairs_name_map.keys())
        result = {'kraken': {}}

        payload = ','.join(pairs)
        response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={payload}')
        if response.status_code == 200:
            response = response.json()
            [result['kraken'].update({self.pairs_name_map[ticker]: value['c'][0]}) for ticker, value in response['result'].items()]
            r.publish('tickers', json.dumps(result))

        # while pairs:
        #     new_pair = pairs.pop(0)
        #     payload = payload.join([f'{new_pair}'])
        #     # logging.info(payload)
        #     response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={payload}')
        #     try:
        #         if response.status_code == 200:
        #             response = response.json()
        #             # logging.info(response)
        #             [result['kraken'].update({pairs_name_map[ticker]: value['c'][0]}) for ticker, value in response['result'].items()]
        #             r.set('kraken', json.dumps(result, indent=' '))
        #             logging.info(result)
        #     except:
        #         defect.append(new_pair)
        #         # logging.info('defect: %s', new_pair)
        #         # temp = payload.split(',')
        #         # defect.append(temp[0])
        #         # payload = ','.join(temp[1::])
        #         payload.replace(f'{new_pair},', '')
        #         # break
        #     # else:
        #     #     logging.info(defect)
        #     #     break
        # logging.info(defect)

    def process_message(self, msg):
        # msg = [2257, [['0.82510000', '39.59475000', '1613428033.364492', 'b', 'm', '']], 'trade', 'USDT/EUR']
        if isinstance(msg, list):
            pair = msg[-1].replace(
                    'XBT', 'BTC').replace(
                    'XDG', 'DOGE').replace(
                    'XXML', 'XML')
            price = msg[1][-1][0]
            self.data.update({pair: price})
            r.publish('tickers', json.dumps({self.stock_name: self.data}))


    def subscription(self):
        self.ws.subscribe_public(
            subscription = {
                'name': 'trade'
            },
            pair = list(self.pairs_name_map.values()),
            callback = self.process_message
        )
        self.ws.start()


if __name__=="__main__":
    Kraken()