import json
import re

from flask_restful import Resource, reqparse, Api, request
from config import STOCKS
from flask import Blueprint, Response, jsonify, render_template
from pprint import pprint

from app import app, r
from models import Kraken, Binance
from operations import Aggregate


api = Api(app, prefix='/api/v1')

parser = reqparse.RequestParser(bundle_errors=True)


def args_to_parser(validator, params, location):
    parser.args.clear()
    for field, valid_param in validator[params].items():
        parser.add_argument(field, **valid_param, location=location)
    return parser


def ticker_validate(ticker):
    if bool(re.match(r'[A-Z.]{2,}/[A-Z.]{2,}', ticker)):
        return ticker
    elif not ticker:
        return None
    else:
        raise ValueError('Ticker format must be two or more symbol diveded by / like: BTC/ETH')

def check_stock(stock):
    if stock in STOCKS:
        return stock
    if not stock:
        return None
    else:
        raise ValueError('This field type must be the name of stock like: kraken or binance')

args_validator = {
    'filters': {
        'ticker': dict(type=ticker_validate, required=False, help='{error_msg}'),
        'stock': dict(type=check_stock, required=False, help='{error_msg}'),
    }
}

class TickerApi(Resource):

    def get(self):
        parser = args_to_parser(args_validator, 'filters', 'args')
        data = parser.parse_args()
        ticker, stock = data['ticker'], data['stock']
        api_data = r.get('aggregated')
        result = []
        if api_data:
            api_data = json.loads(api_data)
            if ticker and stock:
                result.append({
                    'ticker':ticker,
                    stock: api_data[stock].get(ticker, None)   
                })
            elif stock:
                for _ticker, price in api_data[stock].items():
                    result.append({
                        'ticker': _ticker,
                        stock: price
                    })
            elif ticker:
                temp = {'ticker': ticker,}
                for _stock, data in api_data.items():
                    temp.update({_stock: data.get(ticker, None)})
                result.append(temp)
            else:
                temp = {}
                for _stock, data in api_data.items():
                    for _ticker, price in data.items():
                        if not temp.get(_ticker):
                            temp[_ticker] = {'ticker': _ticker,}
                        temp[_ticker].update({_stock: price})
                for ticker, values in temp.items():
                    for stock in api_data.keys():
                        if not values.get(stock):
                            temp[ticker][stock] = None
                result = [dict(i) for i in temp.values()]
        return {
                'status': 'success',
                'data': result}, 200


api.add_resource(TickerApi, '/monitoring')


def get_all_pairs():
	return list(set([
		*Kraken().get_pairs(),
		*Binance().get_pairs()
	]))


@app.route('/dashboard')
def index():
	# form = PairsStockForm()
	return render_template('index.html', 
		root_url=request.url_root,
		tickers_count=len(get_all_pairs()))


@app.route('/monitoring_stream')
def kraken():
	return Response(
        status='200',
        content_type='application/json',
        response=Aggregate().run())
