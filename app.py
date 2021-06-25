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
    ''' The default route of the webserver.
        Used to deliver the HTML page for file upload and also used to display the parsed info.
    '''
    if filename is not None and filename in data['Documents']:
        json_text = api_serialized_data(filename)
        return flask.render_template('page.html', filename=filename, json_text=json_text)
    return flask.render_template('page.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    ''' The upload API route used to upload XML files.
        Parses the data from the XML and saves it in the text file database.
    '''
    f = flask.request.files['filename']
    parsed_xml = xml_parser.parse_xml(f)
    plaintiff_index = data['Plaintiffs']['Current_Index'] = data['Plaintiffs']['Current_Index'] + 1
    defendant_index = data['Defendants']['Current_Index'] = data['Defendants']['Current_Index'] + 1
    data['Plaintiffs'][str(plaintiff_index)] = parsed_xml['Plaintiff']
    data['Defendants'][str(defendant_index)] = parsed_xml['Defendant']
    data['Documents'][f.filename] = {'Plaintiff_Id': str(plaintiff_index),
                                     'Defendant_Id': str(defendant_index)}
    data['Documents']['Current_Index'] = data['Documents']['Current_Index'] + 1
    data['Documents'][f.filename]['Document_Id'] = str(
        data['Documents']['Current_Index'])
    save_database()
    return flask.redirect('/files/' + f.filename)


@app.route('/api/file/<filename>', methods=['GET'])
def retrieve(filename):
    ''' The GET JSON API route to get the extracted data of a file as a JSON
        Returns an empty JSON if there is not data regarding a file in the database
     '''
    if filename is not None and filename in data['Documents']:
        return api_serialized_data(filename)
    return {}


def api_serialized_data(filename):
    '''Serializes the data from the database into JSON API format'''

    plaintiff_id = str(data['Documents'][filename]['Plaintiff_Id'])
    defendant_id = str(data['Documents'][filename]['Defendant_Id'])
    document_id = str(data['Documents'][filename]['Document_Id'])
    document = {
        "$type": "document",
        "id": document_id,
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
    serialized = json_api_doc.serialize(document)
    return serialized


def initialize_database():
    ''' Used to initialize the database
    '''
    global data
    with open('database.txt', 'w') as outfile:
        data = {'Documents': {'Current_Index': 0},
                'Plaintiffs': {'Current_Index': 0},
                'Defendants': {'Current_Index': 0}}
        json.dump(data, outfile)


def load_database():
    ''' Attempts to load the database and initializes it if it doesn't exist
    '''
    global data
    try:
        with open('database.txt') as json_file:
            data = json.load(json_file)
            if 'Documents' not in data or 'Plaintiffs' not in data or 'Defendants' not in data:
                initialize_database()
    except FileNotFoundError:
        initialize_database()


def save_database():
    ''' Saves new data to the database, not atomically safe since using text file
    '''
    global data
    with open('database.txt', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    ''' Loads the database and starts the webserver
    '''
    load_database()
    app.run(debug=True)
