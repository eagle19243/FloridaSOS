import json
from flask import Flask, send_from_directory, render_template
from .util import load_config
from .database import Database
from .scraper import Scraper

APP = Flask(__name__, static_folder='static', static_url_path='/static')
CFG = load_config()
SCRAPER = Scraper(CFG)


def get_app():
    SCRAPER.run()

    return APP


# Flask default route to catch all unhandled URLs
# https://stackoverflow.com/questions/13678397/python-flask-default-route-possible
@APP.route('/', defaults={'path': ''})
@APP.route('/<path:path>')
def index(path=None):
    return render_template('index.html')


@APP.route('/get_corps', methods=['POST'])
def get_corps():
    db = Database(CFG)
    corps = db.get_data()

    return json.dumps(corps)


@APP.route('/get_csv', methods=['GET', 'POST'])
def get_csv():
    return send_from_directory(APP.static_folder, 'output.csv', as_attachment=True)
