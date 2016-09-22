#!/usr/bin/env python

from flask import Flask
from flask import url_for
from flask import request
from flask import Response
from flask import render_template

import json
import demjson

app = Flask(__name__)

OP = {"GET" : "returns list of all objects",
      "PUT" : "add item",
      "POST" : "updates item",
      "DELETE" : "deletes item"}

ACCEPT_OP = ['GET', 'PUT', 'POST', 'DELETE']

STORAGE = {"string":["hello", "world", ],
           "int":[1, 2, 3],
           "float":[1.1, 2.2, 3.3]}


@app.route("/")
def api_root():
    return "Welcome"


def _help_index(keyword=None):
    content = list()
    for op in ACCEPT_OP:
        content.append("<p><a href=\"%s\">usage for %s</a> ...</p>"
                       % (url_for('api_helps') + "/" + op, op))
    html = "\n".join(content)
    return html


def _console_index(keyword=None):
    content = list()
    for op in ACCEPT_OP:
        content.append("<p><a href=\"%s\">op console for %s</a> ...</p>"
                       % (url_for('api_helps') + "/" + op, op))
    html = "\n".join(content)
    return html


def _log_index(keyword=None):
    html = """
      <p>timestamp of request...</p>
      <p>received data...</p>
      <p>visualization of structure content...</p>
"""
    return html


@app.route("/help")
def api_helps():
    html_body = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Help</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="%s">
</head>
<body>

<div class="jumbotron text-center">
  <h1>Web Console for RESTful API </h1>
  <p>a simple web ui to access and manipulate hosted resource</p>
</div>

<div class="container">
  <div class="row">
    <div class="col-sm-3">
      <h3>Help</h3>
%s
    </div>
    <div class="col-sm-3">
      <h3>Operation Console</h3>
%s
    </div>
    <div class="col-sm-3">
      <h3>Log</h3>
%s
    </div>
  </div>
</div>
</body>
</html>
""" % (url_for('static', filename='css/bootstrap.css'),
       _help_index(), _console_index(), _log_index())
    return html_body


@app.route("/help/<operator>")
def api_help(operator):
    if operator not in OP:
        return "undefined for %s" % operator
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Help for %s</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="%s">
</head>
<body>

<div class="container">
  <h3>Usage of %s</h3>
  <p>%s</p>
</div>

</body>
</html>
""" % (operator,
       url_for('static', filename='css/bootstrap.css'),
       operator,
       OP[operator])
    return html


# ===
# /api/v1
# ===
@app.route("/api/<version>", methods=ACCEPT_OP)
def api(version):
    if version != "v1":
        return "version not supported yet"
    _method = request.method
    if _method not in ACCEPT_OP:
        return "method not supported yet"
    response_body = ""
    if _method == "GET":
        response_body = _api_get()
    else:
        response_body = _handle_api_and_json(_method,
                                             request.headers,
                                             request.data)
    # return JSON
    resp = Response(response_body)
    resp.headers['Content-type'] = "application/json"
    return resp


def _handle_api_and_json(method, headers, data):
    """
    :param method:  PUT/POST/DELETE
    :param headers:  Content-Type
    :param data:  JSON
    :return: JSON
    """
    if not _is_content_type_json(headers):
        return demjson.encode({'status': 'ERROR'})
    if method == "PUT":
        return _api_put(data)
    elif method == "POST":
        return demjson.encode({'status': 'NOTYET', 'OP': method})
    elif method == "DELETE":
        return demjson.encode({'status': 'NOTYET', 'OP': method})
    return demjson.encode({'status': 'ERROR'})


def _is_content_type_json(header_dict):
    header_name = None
    for name in header_dict.keys():
        if name.lower() == 'content-type':
            header_name = name
            break
    if "json" in (header_dict[header_name]).lower():
        return True
    return False


# ===
# api implementation
# ===
def _api_get():
    # return "</br>".join(STORAGE.keys())
    json_meta = demjson.encode(STORAGE)
    return json_meta


def _api_put(json_meta=None):
    input_json = demjson.decode(json_meta)
    return demjson.encode({'status': 'ECHO',
                           'OP': "PUT",
                           'INPUT': input_json})


def _api_post(json_meta=None):
    return OP['POST']


def _api_delete(json_meta=None):
    return OP['DELETE']





if __name__ == '__main__':
    app.run(debug=True)
