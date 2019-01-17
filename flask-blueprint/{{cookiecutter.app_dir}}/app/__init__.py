from typing import Text, Tuple

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.routes import {{cookiecutter.blueprint_name}}

app = Flask(__name__)

app.register_blueprint({{cookiecutter.blueprint_name}}.blueprint)

@app.route("/healthcheck")
def healthcheck() -> str:
    # The healthcheck returns status code 200
    return do_healthcheck()


def do_healthcheck():
    return "OK"
