import traceback

from time import sleep
from functools import wraps
from json.decoder import JSONDecodeError
from requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    SSLError
)
from app import logging


def connection_exceptions(system=None):
    """
    Handle ChunkedEncodingError, ConnectionError, SSLError, JSONDecodeError
    """
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            e = ''
            error_content = ''
            status_code = None
            url = args[1]
            tries = 0

            while tries <= 5:
                tries += 1
                logging.info('tries: %s, %s, %s', tries, url, status_code)

                try:
                    r = func(*args, **kwargs)

                    if r is None:
                        r = func(*args, **kwargs)

                    error_content = r.content
                    status_code = r.status_code

                    do_return = True

                    if status_code != 200:
                        logging.error('Error: %s, %s', status_code, url)
                        do_return = False
                        sleep(60*tries)
                    else:
                        r.json()

                    if do_return:
                        return r

                except (ChunkedEncodingError, ConnectionError, SSLError, JSONDecodeError) as err:
                    sleep(60 if tries < 4 else 60 * tries)
                    logging.error(f'decorator exception {err.__class__}', f'{traceback.format_exc()}')
                    e = err

            logging.error('NotImplementedError: %s', e)
            raise NotImplementedError(f'\nWe are here for some reason and returns None'
                                      f'\nerror_content: {error_content}'
                                      f'\ne: {e}'
                                      f'\nstatus_code: {status_code}')
        return wrapper
    return inner_function