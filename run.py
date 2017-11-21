#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Development run script
"""
from app import app
app.run(debug=True, port=app.config['PORT'], threaded=True)
