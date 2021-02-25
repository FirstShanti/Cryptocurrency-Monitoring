import json

from multiprocessing import Process
from time import sleep, time
from pprint import pprint
from redis.exceptions import ConnectionError

from app import r, to_send, logging
from config import STOCKS


class Aggregate(Process):

    def __init__(self):
        Process.__init__(self)


    def run(self):
        global to_send

        pubsub = r.pubsub()
        pubsub.subscribe('tickers')

        if ( aggregated_data := r.get('aggregated') ):
            to_send = json.loads(aggregated_data)
            yield json.dumps(to_send, indent=' ')
        while True:

            try:
                for message in pubsub.listen():
                    if message['data'] != 1:
                        data = json.loads(message['data'])
                        to_send.update(data)
                        #yield json.dumps(to_send, indent=' ')
                        yield (b'-next-'+bytearray(json.dumps(to_send).encode()))
                        #sleep(0.001)
                    else:
                        continue
            except ConnectionError as e:
                logging.error('ConnectionError')
                continue
            except AttributeError as e:
                pubsub = r.pubsub()
                pubsub.subscribe('tickers')
                continue

