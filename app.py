import os
import logging
# import redis
from flask import Flask
from config import Development, Production, env, url
from models import Kraken, Binance
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(env[os.environ.get('ENVIRONMENT', 'Development')])
CORS(app, resorces={r'/d/*': {"origins": '*'}})
# redis_client = redis.Redis(host='127.0.0.1')


API = {
	'kraken': Kraken(),
	# 'binance': Binance()
}
msgs = []