
import json
import os

import flask
import requests

from pysword import Module


app = flask.Flask(__name__)

@app.route('/')
def root():
  return flask.render_template('main.html')

@app.route('/proxy', methods=['POST'])
def proxy():
  data = json.loads(flask.request.data)
  try:
      html = Module(data['module']).read(data['book'], data['chapter'])
  except Exception as e:
      print e
  return flask.jsonify({'html': html})

if __name__ == "__main__":
  app.run(port=8000)
