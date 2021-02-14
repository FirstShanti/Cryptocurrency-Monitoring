from flask import render_template, Response, stream_with_context
from websocket import create_connection

from app import app, API
from operations import Generate



@app.route('/my-large-page.html')
def render_large_template():
    rows = iter_all_rows()
    return Response(stream_template('the_template.html', rows=rows))


@app.route('/index')
def index():
	return render_template('index.html') #,


@app.route('/kraken')
def kraken():

	return Response(
        status='200',
        content_type='application/json',
        response=Generate('kraken', ['XBT/USD', 'TBTC/ETH', 'DAI/EUR', 'CRV/XBT']).run())


@app.route('/binance')
def binance():
	pass