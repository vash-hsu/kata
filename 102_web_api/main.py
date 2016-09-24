#!/usr/bin/env python

from flask import Flask
from flask import url_for
from flask import request
from flask import Response
from flask import render_template
from flask import send_from_directory

import demjson
import hashlib

app = Flask(__name__)

OP = {"GET": "returns list of all objects",
      "PUT": "updates item",
      "POST": "adds item",
      "DELETE": "deletes item"}

ACCEPT_OP = ['GET', 'PUT', 'POST', 'DELETE']

STORAGE = {
    "123456789": {'hello': 'world'},
    "test_data": {'test': 'data'}
}


@app.route("/")
def api_root():
    html_body = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>RESTful Demo Site</title>
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
                       % (url_for('console') + "/" + op.lower(), op))
    html = "\n".join(content)
    return html


def _log_index(keyword=None):
    html = """
      <p>timestamp of request...</p>
      <p>received data...</p>
      <p>visualization of structure content...</p>
"""
    return html


@app.route("/console")
@app.route("/console/<opcode>")
def console(opcode='get'):
    if opcode in ('get', 'post', 'delete'):
        return render_template("get.html",
                               resource_url="/api/v1/resource",
                               ui_put_url="/ui/put",
                               ui_delete_url="/ui/delete")
    else:
        return render_template("get.html", target_url="wrong")


@app.route("/ui/<path:path>")
def form_ui(path):
    terms = path.split('/')
    if len(terms) != 2:
        return "not supported", 400
    action, resource_id = terms
    if action in ('put', 'delete'):
        return render_template("form_edit.html",
                               resource_url="/api/v1/resource",
                               action_type=action,
                               resource_id=resource_id)


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
  <h1>Help Page for RESTful API</h1>
  <p>a simple web page to tell how to integrate provided APIs</p>
</div>

<div class="container">
  <div class="row">
    <div class="col-sm-3">
      <h3>Help</h3>
%s
    </div>
  </div>
</div>
</body>
</html>
""" % (url_for('static', filename='css/bootstrap.css'),
       _help_index())
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


@app.route("/static/<path:file_path>")
def send_static(file_path):
    return send_from_directory("static", file_path)


def _api_split_version_resource(string_path):
    """
    :param string_path:   v1/resource
    :return:  ['v1', 'resource']
    """
    terms = string_path.split('/')
    if len(terms) >= 2:
        return terms
    else:
        return [string_path, ]


# ===
# /api/v1/resource
# ===
@app.route("/api/<path:resource_path>", methods=ACCEPT_OP)
def api(resource_path):
    terms = _api_split_version_resource(resource_path)
    if len(terms) < 2:
        return "undefined path /api/%s" % resource_path, 404
    api_version = terms[0]
    res_type = terms[1]
    resource_id = None
    if len(terms) == 3:
        resource_id = terms[2]
    if api_version != "v1":
        return "API version not supported yet"
    if res_type != "resource":
        return "resource type not defined"
    # depends on request method
    _method = request.method
    if _method not in ACCEPT_OP:
        response_body = demjson.encode({"status": "-1",
                                        'reason': '%s not supported' % _method})
    elif _method == "GET":
        response_body = _api_get(resource_id)
    else:
        response_body = _handle_api_and_json(_method,
                                             request.headers,
                                             request.data,
                                             resource_id)
    # return JSON
    resp = Response(response_body)
    resp.headers['Content-type'] = "application/json"
    return resp


def _handle_api_and_json(method, headers, data, resource_id=None):
    """
    :param method:  PUT/POST/DELETE
    :param headers:  Content-Type
    :param data:  JSON
    :param resource_id:  string
    :return: JSON
    """
    error_msg = []
    json_in_dict = dict()
    if not _is_content_type_json(headers):
        error_msg.append('should provide content-type as application/json')
    else:
        try:
            # print "DM:", repr(data)
            json_in_dict = demjson.decode(data)
        except BaseException:
            error_msg.append('fail to decode incoming json')
    if len(error_msg) == 0:
        if method == "PUT":
            if _is_valid_id(resource_id):  # update legacy
                return _api_put(json_in_dict, resource_id)
            else:
                error_msg.append("PUT needs existent resource_id")
        elif method == "POST":  # insert new
            if resource_id is None or len(resource_id) == 0:
                return _api_post(json_in_dict)
            else:
                error_msg.append("POST needs not user-specified resource_id")
        elif method == "DELETE":
            if _is_valid_id(resource_id):  # delete legacy
                return _api_delete(json_in_dict, resource_id)
            else:
                error_msg.append("DELETE needs existent resource_id")
        else:
            error_msg.append('not support method with %s' % repr(resource_id))
    return demjson.encode({'status': str(0-len(error_msg)),
                           'reason': error_msg})


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

# Get: return list of all objects' names
def _api_get(resource_id=None):
    """
    :param resource_id: string
    :return:
        'status', number of elements in STORAGE
        'storage', elements in STORAGE
    """
    dict_for_return = dict()
    if not resource_id: # return all elements' name
        dict_for_return['status'] = len(STORAGE)
        dict_for_return['listing'] = STORAGE.keys()
    elif resource_id in STORAGE:
        dict_for_return['status'] = '1'
        dict_for_return['value'] = STORAGE[resource_id]
    else: # unrecognized id
        dict_for_return['status'] = '0'
    json_meta = demjson.encode(dict_for_return)
    return json_meta


def _is_valid_id(string_id):
    if not string_id:
        return False
    if string_id in STORAGE:
        return True
    return False


def _update_to_internal_storage(id, data):
    STORAGE[id] = data


def _remove_from_internal_storage(id):
    del STORAGE[id]


def _get_sha1_in_string(data):
    sha1 = hashlib.sha1()
    sha1.update(repr(data))
    return sha1.hexdigest()


# PUT: updates item
# update name:value, where name should be in STORAGE already
def _api_put(json_meta, resource_id=None):
    """
    :param json_meta: {"item name": item value}
    :param resource_id: string
    :return: json
    """
    _update_to_internal_storage(id=resource_id, data=json_meta)
    status = '1'
    return_data = demjson.encode({'status': status, 'id': resource_id})
    return return_data


# POST: adds item
# update name:value, where name was created in runtime
def _api_post(json_meta):
    """
    :param json_meta:
    :return: json
    """
    resource_id = _get_sha1_in_string(json_meta)
    _update_to_internal_storage(id=resource_id, data=json_meta)
    status = '1'
    return_data = demjson.encode({'status': status, 'id': resource_id})
    return return_data


# DELETE: deletes item
def _api_delete(json_meta, resource_id):
    """
    :param json_meta:
    :param resource_id:
    :return:
    """
    _remove_from_internal_storage(resource_id)
    status = '1'
    return_data = demjson.encode({'status': status, 'id': resource_id})
    return return_data


if __name__ == '__main__':
    app.run(debug=False)
