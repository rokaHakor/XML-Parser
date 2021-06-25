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
    if filename is not None and filename in data['Documents']:
        json_text = api_serialized_data(filename)
        return flask.render_template('page.html', filename=filename, json_text=json_text)
    return flask.render_template('page.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    f = flask.request.files['filename']
    parsed_xml = xml_parser.parse_xml(f)
    plaintiff_index = data['Plaintiffs']['Current_Index'] = data['Plaintiffs']['Current_Index'] + 1
    defendant_index = data['Defendants']['Current_Index'] = data['Defendants']['Current_Index'] + 1
    data['Plaintiffs'][plaintiff_index] = parsed_xml['Plaintiff']
    data['Defendants'][defendant_index] = parsed_xml['Defendant']
    data['Documents'][f.filename] = {'Plaintiff_Id': plaintiff_index,
                                     'Defendant_Id': defendant_index}
    save_database()
    return flask.redirect('/files/' + f.filename)


@app.route('/api/file/<filename>', methods=['GET'])
def retrieve(filename):
    if filename is not None and filename in data['Documents']:
        return api_serialized_data(filename)
    return {}


def api_serialized_data(filename):
    plaintiff_id = data['Documents'][filename]['Plaintiff_Id']
    defendant_id = data['Documents'][filename]['Defendant_id']
    document = {
        "$type": "Document",
        "id": "1",
        "filename": filename,
        "plaintiff": {
            "$type": "people",
            "id": plaintiff_id,
            "name": data['Plaintiffs'][plaintiff_id]
        },
        "defendant": {
            "$type": "corporation",
            "id": defendant_id,
            "name": data['Defendants'][defendant_id]
        }
    }
    return json_api_doc.serialize(document)


def initialize_database():
    global data
    with open('database.txt', 'w') as outfile:
        data = {'Documents': {'Current_Index': 0},
                'Plaintiffs': {'Current_Index': 0},
                'Defendants': {'Current_Index': 0}}
        json.dump(data, outfile)


def load_database():
    global data
    try:
        with open('database.txt') as json_file:
            data = json.load(json_file)
            if 'Documents' not in data or 'Plaintiffs' not in data or 'Defendants' not in data:
                initialize_database()
    except FileNotFoundError:
        initialize_database()


def save_database():
    global data
    with open('database.txt', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    load_database()
    app.run(debug=True)
