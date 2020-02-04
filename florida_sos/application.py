"""application.py -- top-level web application for florida_sos.
"""
from .util import load_config
from .web import get_app

# Init Flask app
APP = get_app()
