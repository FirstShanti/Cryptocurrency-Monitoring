import logging
import os
import json
import traceback
import redis

from multiprocessing import Process
from redis.exceptions import ConnectionError


logging.basicConfig(level=logging.DEBUG)
logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def aggregate():
    
    r = redis.StrictRedis(
        host=os.environ.get('REDIS_URL'),
        port=6379,
        db=0,
        password=os.environ.get('REDIS_PASSWORD', None))

    logging.info('Redis conected')
    pubsub = r.pubsub()
    pubsub.subscribe('tickers')
    logging.info('Pubsub conected')

    to_send = {
        'kraken': {},
        'binance': {}
    }

    while True:
        try:
            for message in pubsub.listen():
                if message['data'] != 1:
                    (stock, data), = json.loads(message['data']).items()
                    to_send[stock].update(data)
                    r.set('aggregated', json.dumps(to_send, indent=' '))
                    # yield json.dumps(to_send, indent=' ')
                    # sleep(0.001)
            else:
                continue
        except ConnectionError as e:
            continue
        except Exception as e:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    p = Process(target=aggregate)
    p.start()
    p.join()
    