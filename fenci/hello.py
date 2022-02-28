from flask import Flask, redirect, url_for, request
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/HelloWorld/<guest>')
def hello_world(guest):
    return 'Hello %s World' % guest


@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest


@app.route('/match', methods=['POST'])
def matchKey():
    text = request.json.get('text')
    return main.match(text)


@app.route('/calc', methods=['POST'])
def

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8089)
