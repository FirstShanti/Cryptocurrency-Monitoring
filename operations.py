from flask import render_template, render_template_string, stream_with_context
from multiprocessing import Process
from threading import Thread

from app import app, API, msgs
import logging
from time import sleep
import traceback
import json

class Generate(Process):

    def __init__(self, stock, assets):
        Process.__init__(self)
        self.stock = stock
        self.assets = assets
        self.msgs = {}

    def run(self):
        global API
        global msgs

        ws = API[self.stock]
        ws.subscribe(self.assets)
        ws = ws.ws

        while True:

            res = json.loads(API[self.stock].ws.recv().encode())
            if isinstance(res, list):
                channel_id = res.pop(0)
                price = res.pop(0)
                pair = res.pop(-1)
                self.msgs[channel_id] = {"pair": pair, "price": price["b"][0]}
                yield json.dumps(self.msgs, indent=' ')
