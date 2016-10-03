#!/usr/bin/env python

from flask import Flask, url_for
from flask import request

app = Flask(__name__)


@app.route("/")
def api_root():
    body_array = []
    root_url = "http://" + request.headers["host"]
    body_array.append(root_url + url_for("api_articles"))
    body_array.append(root_url + url_for("api_article", aritcle_id="123456789"))
    body_array.append(root_url + url_for("api_request",
                                         resource_id="123456789"))
    body_array.append(root_url + url_for("api_request",
                                         resource_id="123456789")
                      + "?by=hello&token=world")
    return _prepare_html("Welcome", body_array)


@app.route("/articles")
def api_articles():
    return "List of " + url_for("api_articles")


@app.route("/articles/<aritcle_id>")
def api_article(aritcle_id):
    return "You are reading {}".format(aritcle_id)


# /request/123456789?by=user&token=9999999
@app.route("/request/<resource_id>", methods=["GET", "POST", "PUT", "DELETE"])
def api_request(resource_id):
    for i in request.args:
        print "DM: parameter {} = {}".format(i, request.args[i])
    print "DM: method = {}".format(request.method)
    body_array = []
    if "by" in request.args and "token" in request.args:
        name = request.args["by"]
        token = request.args["token"]
        body_array.append("You are [{}] using [{}] to access [{}]".
                          format(name, token, resource_id))
    else:
        body_array.append("access deny without valid by= and token=")
    body_array.append("http method is [{}]".format(request.method))
    return _prepare_html(resource_id, body_array)


def _prepare_html(title, body_array):
    buffer = """
<!DOCTYPE html>
<html>
<head>
<title>{}</title>
</head>

<body>
<div>
{}
</div>
</body>

</html>
    """.format(title, "</div>\n<div>".join(
        _prepare_hyperlink_for_body(body_array)))
    return buffer


def _prepare_hyperlink_for_body(body_array):
    packed_array = []
    for i in body_array:
        if i.lower().find("http://") == 0:
            packed_array.append("<a href=\"{}\">{}</a>".format(i, i))
        else:
            packed_array.append(i)
    return packed_array


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

