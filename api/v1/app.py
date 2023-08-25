#!/usr/bin/python3
"""start the api"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_app(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """return error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        api_host = getenv("HBNB_API_HOST")
    else:
        api_host = '0.0.0.0'
    if getenv("HBNB_API_PORT"):
        api_port = getenv("HBNB_API_PORT")
    else:
        api_port = '50000'
    app.run(host=api_host, port=api_port, threaded=True)
