import xml_parser
import json
import json_api_doc
import flask
from flask import Flask

app = Flask(__name__)
data = {}

@app.route("/")
@app.route('/files/<filename>')
def index(filename=None):
    if filename is not None:
        json_text = data[filename]
        return flask.render_template('page.html', filename=filename, json_text=json_text)
    return flask.render_template('page.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    f = flask.request.files['filename']
    parsed_tuple = xml_parser.parse_xml(f)
    document = {
        '$type': 'article',
        'id': '1',
        'name': 'Article 1'
    }
    print(json_api_doc.serialize(document))
    save_database()
    return flask.redirect('/files/'+f.filename)


@app.route('/api/file/<filename>', methods=['GET'])
def retrieve(filename):
    parsed_file = data[filename]
    return parsed_file


def load_database():
    global data
    try:
        with open('database.txt') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        with open('database.txt', 'w') as outfile:
            json.dump(data, outfile)


def save_database():
    global data
    with open('database.txt', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    load_database()
    app.run(debug=True)
