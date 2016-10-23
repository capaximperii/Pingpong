# -*- coding: utf-8 -*-
""" Page view
This module provides the API endpoints dashboard UI.
 
"""
import os
from flask import Blueprint, send_file

page = Blueprint('page', __name__)
prefix = 'webapp'

@page.route('/', defaults={'path': 'index.html'})
@page.route('/<path:path>')
def home(path):
	"""
	URL Endpoint for static pages for dashboard
	
	:return: 200 on success
	"""
	return send_file(os.path.join(prefix, path))

