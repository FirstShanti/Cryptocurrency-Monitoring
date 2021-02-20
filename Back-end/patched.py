from gevent import monkey
from view import *

monkey.patch_all()

from app import app
