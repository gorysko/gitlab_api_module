#! /usr/bin/env python
"""Server module, based on flask."""

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world(name=None):
    return render_template('first.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)