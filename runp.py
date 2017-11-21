#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production run script
"""
from app import app
app.run(debug=False, host='0.0.0.0', port=app.config['PORT'], threaded=True)
