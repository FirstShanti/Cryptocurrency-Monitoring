import os
import logging
import json
import redis

from flask import Flask
from config import env, Development, Production, STOCKS


logging.basicConfig(level=logging.DEBUG)
logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(env[os.environ.get('ENVIRONMENT', 'Development')])

r = redis.StrictRedis(
    host=os.environ.get('REDIS_URL'),
    port=6379,
    db=0,
    decode_responses=True,
    password=os.environ.get('REDIS_PASSWORD', 'hgyugyUFYuftyuftr86r6FFyf'))

to_send = {}
