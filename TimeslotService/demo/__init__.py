# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

import TimeslotService


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        TimeslotService.bp,
        url_prefix='/TimeslotService')
    return app

if __name__ == '__main__':
    create_app().run(host = '0.0.0.0', port = 8888,debug=True)