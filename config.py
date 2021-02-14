import os


class Configuration(object):
	DEBUG = False
	SECRET_KEY = os.environ.get('SECRET_KEY')


class Development(Configuration):
	DEBUG = True
	SECRET_KEY = 'secret-very-secret-key'
	PORT = 5555


class Production(Configuration):
	pass


env = {
	'Development': Development,
	'Production': Production
	}

url = {
	'kraken': 'wss://ws.kraken.com',
	'binance': 'wss://stream.binance.com:9443'
}