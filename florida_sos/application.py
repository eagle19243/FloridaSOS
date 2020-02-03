"""application.py -- top-level web application for florida_sos.
"""
from .util import load_config
from .scraper import Scraper
from .web import get_app

# Init config
CFG = load_config()

# Init Scraper
scraper = Scraper(CFG)
scraper.run()

# Init Flask app
APP = get_app()
