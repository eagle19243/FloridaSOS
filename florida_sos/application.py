"""application.py -- top-level web application for florida_sos.
"""
from .web import get_app
# Init Flask app
APP = get_app()
