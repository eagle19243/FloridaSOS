"""application.py -- top-level web application for florida_sos.
"""
import sys
from .web import get_app
# Init Flask app
sys.setrecursionlimit(10**8)
APP = get_app()
