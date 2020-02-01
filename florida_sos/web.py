from flask import Flask, send_from_directory

APP = Flask(__name__, static_folder='static')


def get_app():
    return APP


# Flask default route to catch all unhandled URLs
# https://stackoverflow.com/questions/13678397/python-flask-default-route-possible
@APP.route('/', defaults={'path': ''})
@APP.route('/<path:path>')
def index(path=None):
    return send_from_directory(APP.static_folder, 'index.html')
