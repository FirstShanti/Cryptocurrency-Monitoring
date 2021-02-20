import os


class Configuration(object):
	DEBUG = False
	SECRET_KEY = os.environ.get('SECRET_KEY')


class Development(Configuration):
	DEBUG = True
	SECRET_KEY = 'secret-very-secret-key'
	REDIS_URL = os.environ.get('REDIS_URL')


class Production(Configuration):
	pass


env = {
	'Development': Development,
	'Production': Production
	}

STOCKS = ['kraken', 'binance']