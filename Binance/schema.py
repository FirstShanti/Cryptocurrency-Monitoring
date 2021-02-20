import dataclasses
from typing import List
from dataclasses import dataclass
from collections import deque

import desert
from marshmallow import EXCLUDE, Schema


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

    def serialize(self, pairs):
        return {
            pairs[self.s]: self.c
        }


def parse_data(data, pairs):
    result = {}
    schema = desert.schema(BinanceSchema, meta={"unknown": EXCLUDE})
    # deque(map(lambda x: result.update(schema.load(x).serialize(pairs)), data))
    [result.update(schema.load(x).serialize(pairs)) for x in data]
    return result
