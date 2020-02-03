from flask import Flask, send_from_directory, render_template
from .util import load_config
from .database import Database

APP = Flask(__name__, static_folder='static')
CFG = load_config()

def get_app():
    return APP


# Flask default route to catch all unhandled URLs
# https://stackoverflow.com/questions/13678397/python-flask-default-route-possible
@APP.route('/', defaults={'path': ''})
@APP.route('/<path:path>')
def index(path=None):
    return render_template('index.html')

@APP.route('/get_corps', methods=['POST'])
def get_corps():
    db = Database()
    corps = db.get_corps()

    return corps
