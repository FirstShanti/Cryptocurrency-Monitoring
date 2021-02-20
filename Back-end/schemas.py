import dataclasses
from typing import List
from dataclasses import dataclass

import desert
from marshmallow import EXCLUDE, Schema


@dataclass
class KrakenSchema():
# {
# 's': 'BNBBTC',
# 'f': 107287117,
# 'a': 87409096,
# 'q': '0.44000000',
# 'm': True,
# 'E': 1613423851455,
# 'M': True,
# 'T': 1613423851298,
# 'e': 'aggTrade',
# 'p': '0.00270040',
# 'l': 107287117
# }

    c: List[float]
    pair: str

    def serialize(self):
        return {
            'pair': self.pair,
            'price': str(self.c[0])
    }


@dataclass
class BinanceSchema():
# {'e': '24hrTicker',
# 'E': 1613350220004,
# 's': 'RENUSDT',
# 'p': '-0.09462',
# 'P': '-9.579',
# 'w': '0.92964',
# 'c': '0.89318',
# 'Q': '242',
# 'o': '0.98780',
# 'h': '1.01826',
# 'l': '0.86540',
# 'v': '41676024',
# 'q': '38743542.29000',
# 'O': 1613263800000,
# 'C': 1613350219999,
# 'F': 12152391,
# 'L': 12288965,
# 'n': 136575}
    s: str
    c: str

    def serialize(self):
        return {
            'pair': self.s,
            'price': self.c
        }



schemas = {
    'kraken': KrakenSchema,
    'binance': BinanceSchema
}


def parse_data(stock, data):
    schema = desert.schema(schemas[stock], meta={"unknown": EXCLUDE})
    return [schema.load(i).serialize() for i in data]
