
import json
import os

import flask
import requests

from sword import Module


app = flask.Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('main.html')


@app.route('/proxy', methods=['POST'])
def proxy():
  data = json.loads(flask.request.data)
  html = convert_html(Module(data['module']).read(data['book'], data['chapter']))
  return flask.jsonify({'html': html})


def convert_html(text):
  return text.replace("<q", "<q class=\"q\"").replace("<lb", "<div").replace("type=", "class=")


if __name__ == "__main__":
  app.run(port=8080)
