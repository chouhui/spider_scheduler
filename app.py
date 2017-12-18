# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from routes.api_spider import main as spider_api

from spider_scheduler.routes.index import main as index

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.register_blueprint(spider_api)
app.register_blueprint(index)


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3001,
    )
    app.run(**config)