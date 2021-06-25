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
        document = {
            "$type": "Document",
            "id": "1",
            "filename": filename,
            "plaintiff": {
                "$type": "people",
                "id": "1",
                "name": data[filename]['Plaintiff']
            },
            "defendant": {
                "$type": "corporation",
                "id": "1",
                "name": data[filename]['Defendant']
            }
        }
        json_text = json_api_doc.serialize(document)
        return flask.render_template('page.html', filename=filename, json_text=json_text)
    return flask.render_template('page.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    f = flask.request.files['filename']
    parsed_xml = xml_parser.parse_xml(f)
    data[f.filename] = parsed_xml
    save_database()
    return flask.redirect('/files/' + f.filename)


@app.route('/api/file/<filename>', methods=['GET'])
def retrieve(filename):
    if filename in data:
        document = {
            "$type": "Document",
            "id": "1",
            "filename": filename,
            "plaintiff": {
                "$type": "people",
                "id": "1",
                "name": data[filename]['Plaintiff']
            },
            "defendant": {
                "$type": "corporation",
                "id": "1",
                "name": data[filename]['Defendant']
            }
        }
        json_text = json_api_doc.serialize(document)
        return json_text
    return {}


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
