#! /usr/bin/python3.9

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/pollution_painter/api/')
from pollution_painter_api import app as application
application.secret_key = 'password'