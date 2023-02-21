
from flask import Flask
import time

app = Flask(__name__)


@app.route('/mimi')
def index_mimi():
    time.sleep(2)
    return 'Hello mimi'


@app.route('/bobo')
def index_bobo():
    time.sleep(2)
    return 'Hello bobo'


@app.route('/jiojio')
def index_jiojio():
    time.sleep(2)
    return 'Hello jiojio'


if __name__ == '__main__':
    app.run(threaded=True)