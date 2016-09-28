#!/usr/bin/env python

from flask import Flask
from flask import url_for
from flask import request
from flask import Response
from flask import render_template
from flask import send_from_directory

import demjson
import hashlib
import json
import pprint

import logging
import logging.config


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

# will be initialized by __main__
http_log = None
api_log = None
main_log = None

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

    html_part = """<p><a href =\"{}\">click here to download</a></p>""".\
        format(url_for('static', filename="log/rest_api_server.log"))
    html = """
      <p>(v) timestamp of request...</p>
      <p>(v) received data...</p>
      <p>(v) visualization of structure content...</p>
      <p>{}</p>
""".format(html_part)
    return html


@app.route("/console")
@app.route("/console/<opcode>")
def console(opcode='get'):
    if opcode in ('get', 'put', 'delete'):
        return render_template("get.html",
                               resource_url="/api/v1/resource",
                               ui_put_url="/ui/put",
                               ui_delete_url="/ui/delete",
                               ui_theme=opcode)
    elif opcode == 'post':
        return render_template("form_post.html",
                               resource_url="/api/v1/resource")
    else:
        http_log.warning("not support action {}".format(repr(opcode)))
        return "", 404


def _get_referer_from_headers(headers):
    """
    :param headers:  dict
    :return:  string with referer url or empty string
    """
    previous_url = ""
    for i in headers.keys():
        if i.lower() == "referer":
            previous_url = headers[i]
            break
    return previous_url


@app.route("/ui/<path:path>")
def form_ui(path):
    previous_url = _get_referer_from_headers(request.headers)
    terms = path.split('/')
    if len(terms) == 1 and terms[0] == 'post':
        return render_template("form_post.html",
                               resource_url="/api/v1/resource",
                               referer_url=previous_url)
    if len(terms) != 2:
        http_log.warning("not support {}".format(repr(path)))
        return "not supported", 404
    action, resource_id = terms
    if action in ('put',):
        return render_template("form_edit.html",
                               resource_url="/api/v1/resource",
                               put=resource_id,
                               referer_url=previous_url)
    if action in ('delete',):
        return render_template("form_edit.html",
                               resource_url="/api/v1/resource",
                               delete=resource_id,
                               referer_url=previous_url)
    else:
        http_log.warning("not support action {}".format(repr(action)))
        return "not supported", 404


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


# ===
# /api/v1/resource
# ===
@app.route("/api/<path:resource_path>", methods=ACCEPT_OP)
def api(resource_path):
    terms = _api_split_version_resource(resource_path)
    if len(terms) < 2:
        http_log.warning("undefined path /api/{}".format(resource_path))
        return "undefined path /api/%s" % resource_path, 404
    api_version = terms[0]
    res_type = terms[1]
    resource_id = None
    # logging for business logic
    http_log.info('request method: {}'.format(request.method))
    http_log.info('request full_path: {}'.format(request.full_path))
    if len(request.args) > 0:
        http_log.info('request args: {}'.format(repr(request.args)))
    # http_log.info('request headers: {}'.format(repr(request.headers)))
    for i in request.headers:
        http_log.info('request header: {}={}'.format(i[0], i[1]))
    http_log.info('request body: {}'.format(repr(request.data)))
    if len(request.data) > 0:
        http_log.debug("pretty print\n{}".
                       format(_pretty_json_in_text(request.data)))
    #
    if len(terms) == 3:
        resource_id = terms[2]
    if api_version != "v1":
        http_log.warning("not recognize api version {}".format(api_version))
        return "API version not supported yet"
    if res_type != "resource":
        http_log.warning("not recognize resource type {}".format(res_type))
        return "resource type not defined"
    # depends on request method
    _method = request.method
    if _method not in ACCEPT_OP:
        response_body = demjson.encode({"status": "-1",
                                        'reason': '%s not supported' % _method})
    elif _method == "GET":
        response_body = _api_get(resource_id)
    elif _method == "DELETE":
        response_body = _api_delete(resource_id)
    else:
        response_body = _handle_api_and_json(_method,
                                             request.headers,
                                             request.data,
                                             resource_id)
    # return JSON
    resp = Response(response_body)
    resp.headers['Content-type'] = "application/json"
    for i in resp.headers.keys():
        http_log.info("response header: {}={}".format(i, resp.headers[i]))
    http_log.info("response body = {}".format(response_body))
    http_log.debug("pretty print\n{}".
                   format(_pretty_json_in_text(response_body)))
    return resp


def _handle_api_and_json(method, headers, data, resource_id=None):
    """
    :param method:  PUT/POST
    :param headers:  Content-Type
    :param data:  JSON
    :param resource_id:  string
    :return: JSON
    """
    error_msg = []
    json_in_dict = dict()
    if not _is_content_type_json(headers):
        error_text = 'should provide content-type as application/json'
        error_msg.append(error_text)
        http_log.debug(error_text)
    else:
        try:
            json_in_dict = demjson.decode(data)
        except BaseException:
            error_text = "fail to decode incoming json"
            error_msg.append(error_text)
            http_log.debug(error_text)
            http_log.warning("fail to decode {}".format(repr(data)))
    if len(error_msg) == 0:
        if method == "PUT":
            if _is_valid_id(resource_id):  # update legacy
                return _api_put(json_in_dict, resource_id)
            else:
                error_msg.append("PUT needs existent resource_id")
                http_log.warning("fail to put {} because it\'s not existent"
                                 .format(resource_id))
        elif method == "POST":  # insert new
            if resource_id and len(resource_id) > 0:
                if _is_valid_id(resource_id):
                    http_log.warning("not allow existent id {} for post".
                                     format(resource_id))
                    error_msg.append("not allow existent id {} for post".
                                     format(resource_id))
                else:
                    http_log.debug("post with user-defined resource id {}".
                                   format(resource_id))
                    return _api_post(json_in_dict, resource_id=resource_id)
            else:
                return _api_post(json_in_dict)
        else:
            error_msg.append('not support method with %s' % repr(resource_id))
            http_log.warning("not support method {} on resource_id {}".
                             format(method, repr(resource_id)))
    return demjson.encode({'status': 0-len(error_msg),
                           'reason': error_msg})
    # return demjson.encode({'status': str(0-len(error_msg)),
    #                       'reason': "; ".join(error_msg)})


# ===
# utility
# ===

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


def _is_content_type_json(header_dict):
    header_name = None
    for name in header_dict.keys():
        if name.lower() == 'content-type':
            header_name = name
            break
    if "json" in (header_dict[header_name]).lower():
        return True
    return False


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


def _pretty_json_in_text(meta):
    result = ""
    if isinstance(meta, str) or isinstance(meta, unicode):
        try:
            result = json.dumps(json.loads(meta), indent=4, sort_keys=True)
        except BaseException as err:
            print "DM:", repr(err.message)
            printer = pprint.PrettyPrinter(indent=4, width=1)
            result = printer.pformat(meta)
    else:
        printer = pprint.PrettyPrinter(indent=4, width=1)
        result = printer.pformat(meta)
    return result


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
        api_log.info("getting all list: {}".
                      format(demjson.encode(dict_for_return['listing'])))
    elif resource_id in STORAGE:
        dict_for_return['status'] = 0
        dict_for_return['value'] = STORAGE[resource_id]
        api_log.info("getting content of {}: {}".
                     format(resource_id,
                            demjson.encode(dict_for_return['value'])))
    else: # unrecognized id
        dict_for_return['status'] = -1
        reason = "fail to get {}, which is nonexistent".format(resource_id)
        dict_for_return['reason'] = [reason, ]
        api_log.warning(reason)
    json_meta = demjson.encode(dict_for_return)
    #
    if dict_for_return['status'] > 0:
        api_log.info("success on get operation, responding {}".
                     format(json_meta))
    else:
        api_log.info("success on get operation, responding {}".
                     format(json_meta))
    return json_meta


# PUT: updates item
# update name:value, where name should be in STORAGE already
def _api_put(json_meta, resource_id=None):
    """
    :param json_meta: {"item name": item value}
    :param resource_id: string
    :return: json
    """
    api_log.info("putting {} with {}".
                 format(resource_id, demjson.encode(json_meta)))
    _update_to_internal_storage(id=resource_id, data=json_meta)
    status = 0
    return_data = demjson.encode({'status': status, 'value': resource_id})
    api_log.info("success({}) to put resource id = {}".
                 format(status, resource_id))
    return return_data


# POST: create/adds item
# update name:value, where name was created in runtime
def _api_post(json_meta, resource_id=None):
    """
    :param json_meta:
    :param resource_id: if not provided, use sha1 of json instead
    :return: json
    """
    if not resource_id:
        resource_id = _get_sha1_in_string(json_meta)
        while _is_valid_id(resource_id):  # to avoid collision
            resource_id = _get_sha1_in_string(resource_id)
    api_log.debug("posting {} with {}".format(resource_id,
                                              demjson.encode(json_meta)))
    _update_to_internal_storage(id=resource_id, data=json_meta)
    status = 0
    return_data = demjson.encode({'status': status, 'value': resource_id})
    api_log.info("success({}) to post resource id = {}".format(status,
                                                               resource_id))

    return return_data


# DELETE: deletes item
def _api_delete(resource_id):
    """
    :param json_meta:
    :param resource_id:
    :return:
    """
    if not _is_valid_id(resource_id):
        msg = "not allow to delete resource_id {}".format(repr(resource_id))
        status = -1
        return_data = demjson.encode({'status': status,
                                      'reason': [msg, ]})

        http_log.warning(msg)
    else:
        api_log.info("deleting {}".format(resource_id))
        _remove_from_internal_storage(resource_id)
        status = 0
        return_data = demjson.encode({'status': status, 'value': resource_id})
        api_log.info("success({}) to delete resource id = {}".format(status,
                                                                     resource_id))
    return return_data


if __name__ == '__main__':
    logging.config.fileConfig('logger_config.ini')
    # create logger
    http_log = logging.getLogger('httpServer')
    api_log = logging.getLogger('restAPI')
    main_log = logging.getLogger('main')
    #
    app.run(debug=False, host="0.0.0.0")
