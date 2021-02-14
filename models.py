import traceback
import requests
from datetime import datetime, timedelta
from websocket import create_connection

# from app import logging, redis_client
from decorators import connection_exceptions
from config import url
import logging
from pprint import pprint
import json

class Stock():

	STOCK_NAME: str
	ASSETS_LIST_URL: str
	WS_URL: str
	LAST_UPDATE: datetime
	REDIS_ASSETS_ACTUAL: str
	REDIS_ASSETS_SUBSCRIBE: str

	assets_list_raw: list = []
	assets_pairs: list = []
	# Format of values in assets_pairs must be: 
	# [
	# 		'BTC/ETH', - like human readble(with slash)
	# ]


	def __init__(self):
		# global redis_client
		self.sub = []
		print('init')
		print(self.WS_URL)
		self.assets_list_raw = self.get_raw_assets()
		self.prepare_assets_pairs()
		self.ws = create_connection(self.WS_URL)


	@connection_exceptions()
	def get_raw_assets(self) -> list:
		# print('start connect')
		return requests.get(self.ASSETS_LIST_URL)
		# print('get response: ', self.assets_list_raw)

	def prepare_assets_pairs(self):
		"""
		Response schemes from api differ from stock to stock.
		Therefore, we process the response from them separately for each.
		"""
		pass


	def get_pairs(self):
		is_actual = (datetime.now() - self.LAST_UPDATE).days <=1
		if not is_actual:
		# if not redis_client.get(self.REDIS_ASSETS_ACTUAL):
			self.get_raw_assets()
			self.prepare_assets_pairs()
		return self.assets_pairs


class Kraken(Stock):

	STOCK_NAME = 'kraken'
	ASSETS_LIST_URL = 'https://api.kraken.com/0/public/AssetPairs'
	WS_URL = url[STOCK_NAME]
	# REDIS_ASSETS_ACTUAL = 'kraken_ticket_actual'
	# REDIS_ASSETS_SUBSCRIBE = 'kraken_ticket_sub'


	def prepare_assets_pairs(self):
		try:
			self.assets_pairs = []
			# print(self.assets_list_raw['result'].values())
			# pprint(self.assets_list_raw['result'])
			self.assets_pairs = [x['wsname'] for x in self.assets_list_raw['result'].values() if 'wsname' in x]
			print(self.assets_pairs[0])
			self.LAST_UPDATE = datetime.now()
			# for asset in list(self.assets_list_raw['result'].values()):
				# self.assets_pairs.append(asset['wsname'])
				# redis_client.setex(
				# 	self.REDIS_ASSETS_ACTUAL,
				# 	timedelta(days=1),
				# 	value=True)
		except Exception:
			logging.error('%s', traceback.format_exc())


	def unsubscribe(self):
		if self.sub:
			self.ws.send(json.dumps({
				"event": "unsubscribe",
				"pair": self.sub,
				"subscription": {
					"name": "ticker"
				}}))
			self.sub.clear()


	def subscribe(self, data):
		if self.sub:
			self.unsubscribe()
		payload = []
		for symbol in data:
			if symbol in self.assets_pairs:
				payload.append(symbol)
		# redis_client.sadd(
		# 	self.REDIS_ASSETS_ACTUAL,
		# 	*data)
			self.sub = payload
			print('sub: ', self.sub)
		self.ws.send(json.dumps({
			"event": "subscribe",
			"pair": self.sub,
			"subscription": {
				"name": "ticker"
			}}))
		# return payload


class Binance(Stock):

	STOCK_NAME = 'binance'
	ASSETS_LIST_URL = 'https://api3.binance.com/api/v3/exchangeInfo'
	WS_URL = url[STOCK_NAME]
	# REDIS_ASSETS_ACTUAL = 'binance_ticket_actual'
	# REDIS_ASSETS_SUBSCRIBE = 'binance_ticket_sub'


	def prepare_assets_pairs(self):
		try:
			self.assets_pairs = []
			for asset in self.assets_list_raw['symbols']:
				with_slash = f"{asset['baseAsset']}/{asset['quoteAsset']}"
				self.assets_pairs.append(with_slash)
				self.LAST_UPDATE = datetime.now()
				# redis_client.setex(
				# 	self.REDIS_ASSETS_ACTUAL,
				# 	timedelta(days=1),
				# 	value=True)
		except Exception:
			logging.error('%s', traceback.format_exc())


	def unsubscribe(self):
		self.ws.send(json.load({
			"method": "UNSUBSCRIBE",
			"params": self.sub,
		}))
	# 	return redis_client.sadd(
	# 		self.REDIS_ASSETS_ACTUAL,
	# 		*data)


	def subscribe(self, data):
		if self.sub:
			self.unsubscribe()
		payload = []
		data = list(map(lambda x: x.replace('/', '').upper(), data))
		for symbol in data:
			if symbol in self.assets_list_raw['symbols'].keys():
				payload.append(f"{symbol.lower()}@aggTrade")
		# redis_client.sadd(
		# 	self.REDIS_ASSETS_ACTUAL,
		# 	*data)
			self.sub = payload
		self.ws.send(json.load({
			"method": "SUBSCRIBE",
			"params": self.sub,
		}))




