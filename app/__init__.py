#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Init file for Flask app
Author: Chris Anderson <christian.anderson@stresearch.com>
"""
import os
import sqlite3
from flask import Flask
from flask import g
import logging
from logging.handlers import RotatingFileHandler

##
# Initialize app
#
app = Flask(__name__)
# app = Flask(__name__, static_url_path='')
app.config.from_object('config')

##
# Configure logging
#
if not os.path.isdir('logs'):
    os.mkdir('logs')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')

# File log handler
file_handler = RotatingFileHandler('logs/tile-server.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Stream log handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Can set a different console logging level here
stream_handler.setFormatter(log_formatter)

app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.addHandler(stream_handler)
app.logger.info('tile-server startup')


from app import views  # Place this import at end of file to avoid circular import problems
