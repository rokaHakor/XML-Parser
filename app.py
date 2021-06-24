import json
import re
import xml.etree.ElementTree as ET
import flask
from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route('/files/<filename>')
def index(filename=None):
    return flask.render_template('page.html', filename=filename)


@app.route('/upload', methods=['POST'])
def upload():
    if flask.request.method == 'POST':
        f = flask.request.files['filename']
        return flask.redirect('/files/'+f.filename)


if __name__ == '__main__':
    app.run(debug=True)
