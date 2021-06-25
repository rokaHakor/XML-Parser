# XML Parser

Parses XMLs to find relevant information such as the plaintiff and defendant. Uses Flask as a web framework for the front and back end.

## Requirements
The requirements in located in the requirements.txt file.
Install them all using 'pip install -r requirements.txt'.
Can also be used with a virtual environment by using the commands 'py -3 -m venv venv' and 'venv\Scripts\activate' before installing the requirements.

## Running the Program
Run the app.py program and it will launch a server on http://127.0.0.1:5000/.  
Once on the page upload an .xml file and submit it.
The page will then reload with the relevent information extracted and printed in JSON API format. There will also be a hyperlink to the API GET route with the JSON API directly.
