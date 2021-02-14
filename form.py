from flask_wtf import FlaskForm
from wtforms import SelectField
from app import API


def get_all_pairs():
	all_pairs = list(set([pair for x in API.values() for pair in x.get_pairs()]))


class TicketPairForm(FlaskForm):
    ticket_pair = SelectField('Ticket pair',
        id='pairs',
        choices=get_all_pairs())
    stocks = SelectField('Stocks',
        id='stocks',
        choices=list(API.keys()))