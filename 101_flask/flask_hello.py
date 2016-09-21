#!/usr/bin/env python
# http://flask.pocoo.org/docs/0.11/quickstart/

from flask import Flask
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)


# =====
# route() decorator is used to bind a function to a URL.
# =====

@app.route("/")
def root():
    return "index page"


@app.route("/hello")
def hello():
    return "Hello World!"

# =====
# variable rule
# =====

# string 	accepts any text without a slash (the default)
# int 	accepts integers
# float 	like int but for floating point values
# path 	like the default but also accepts slashes
# any 	matches one of the items provided
# uuid 	accepts UUID strings
@app.route("/user/<string:username>")
def show_user_profile(username):
    return 'User %s' % username


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return "Post %d" % post_id


@app.route("/floating/<float:floating>")
def show_float(floating):
    return '%s' % (str(round(floating*100, 2))) + '%'


@app.route("/show_path/<path:string_path>")
def show_path(string_path):
    return "%s" % string_path

# =====
# Unique URLs / Redirection Behavior
# =====

# accept both /projects and /projecfts/
@app.route("/projects/")
def projects():
    return 'The project page'

# only accept both /about
@app.route("/about")
def about():
    return 'The about page'

# =====
# URL Building
# function name as first argument
# =====

@app.route("/login")
def login():
    return "The login page"

@app.route("/page")
def page():
    function_names = ['root', 'login', 'page']
    content = []
    # name of the function as first argument
    for i in function_names:
        content.append("<a href='%s'>%s</a>" % (url_for(i), i))
    # keyword arguments
    content.append("<a href='%s'>%s</a>" %
                   (url_for("show_user_profile", username="admin"),
                    "user = admin"))
    content.append("<a href='%s'>%s</a>" %
                   (url_for("show_user_profile", username="root"),
                    "user = root"))
    # query string
    # Unknown variable parts are appended to the URL as query parameters.
    content.append("<a href='%s'>%s</a>" %
                   (url_for("show_path", string_path="1/2/3/4"),
                    "show_path / 1/2/3/4"))
    content.append("<a href='%s'>%s</a>" %
                   (url_for("show_path", string_path="bin/cgi",
                            name="value",
                            key="value"),
                    "show_path / bin/cgi ? name=value & key=value"))
    return "<html><body>" + "<br>\n".join(content) + "</body></html>"


# =====
# HTTP method
# By default, a route only answers to GET requests
# If GET is present, HEAD will be added automatically for you
# OPTIONS is implemented for you automatically as well.
# =====
@app.route("/method", methods=["GET", "PUT", "POST"])
def method():
    description = {
        "GET": "The browser tells the server to just get the information "
               "stored on that page and send it. "
               "This is probably the most common method.",
        "PUT": "Similar to POST but the server might trigger "
               "the store procedure multiple times "
               "by overwriting the old values more than once. "
               "Now you might be asking why this is useful, but "
               "there are some good reasons to do it this way. "
               "Consider that the connection is lost during transmission: "
               "in this situation a system between the browser and the server "
               "might receive the request safely a second time "
               "without breaking things. "
               "With POST that would not be possible because "
               "it must only be triggered once.",
        "POST": "The browser tells the server that it wants to post "
               "some new information to that URL and "
               "that the server must ensure the data is stored and "
               "only stored once. "
               "This is how HTML forms usually transmit data to the server.",
        "DELETE": "Remove the information at the given location."
    }
    if request.method not in description:
        return request.method
    return "\n".join(["<html><head><title>", request.method, "</title></head>",
                      "<body>", description[request.method], "</body></html>"])


# =====
# Static Files
# url_for('static', filename='style.css')
# The file has to be stored on the filesystem as static/style.css.
# =====
@app.route("/show_css/")
def show_css():
    html_body = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="%s">
</head>
<body>

<div class="jumbotron text-center">
  <h1>My First Bootstrap Page</h1>
  <p>Resize this responsive page to see the effect!</p>
</div>

<div class="container">
  <div class="row">
    <div class="col-sm-5">
      <h3>Column 1</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
    <div class="col-sm-5">
      <h3>Column 2</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit...</p>
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...</p>
    </div>
  </div>
</div>
</body>
</html>
""" % (url_for('static', filename='css/bootstrap.css'))
    return html_body


# =====
# Rendering Templates
# /this_scirpt_file.py
# /templates          <-- create folder
#    /profile.html    <-- html template
# ---
# more: http://jinja.pocoo.org/docs/dev/templates/
# =====
@app.route("/profile/")
@app.route("/profile/<id>")
def show_detail_profile(id=None):
    return render_template("profile.html", name=id)


# [windows]
# set FLASK_APP=flask_hello.py
# set FLASK_DEBUG=1
# [linux]
# export FLASK_APP=flask_hello.py
# export FLASK_DEBUG=1
# python -m flask run
# python -m flask run --host=0.0.0.0 --port=8080

if __name__ == '__main__':
    app.run(debug=True)
