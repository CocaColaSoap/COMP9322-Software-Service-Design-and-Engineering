#! /usr/bin/env python3
from __future__ import absolute_import

from flask import Flask

import DoctorService


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        DoctorService.bp,
        url_prefix='/DoctorService')
    return app

if __name__ == '__main__':
    create_app().run(host = '0.0.0.0',port=5000,debug=True)