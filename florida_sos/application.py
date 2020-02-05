"""application.py -- top-level web application for florida_sos.
"""
import sys
from .web import get_app
# Init Flask app
sys.setrecursionlimit(10**6)
APP = get_app()
