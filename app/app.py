from flask import Flask, render_template
import json
import os

app = Flask(__name__)

FILE_DIR = os.path.dirname(__file__)
PROP_DATA_PATH = os.path.join(FILE_DIR, 'data/data.json')

@app.route('/')
def hello_world():
    props = load_prop_data(PROP_DATA_PATH)
    return render_template('base.html', props=props)

def load_prop_data(path):
    f = open(path, 'r')
    json_text = f.read()
    f.close()
    return json.loads(json_text)

if __name__ == '__main__':
    app.run(debug=True)
