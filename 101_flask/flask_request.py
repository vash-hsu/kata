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
# HTTP method
# =====
@app.route("/method", methods=["GET", "PUT", "POST"])
def method():
    if request.method in ["PUT", "POST"]:
        return request.method, 301
    else:
        # default 200
        return request.method


# =====
# Accessing Request Data
# =====
def valid_login(username, password):
    if username == password:
        return True
    return False


def log_the_user_in(username):
    return "Hello %s!" % username


# /login
# -----
# POST /login HTTP/1.1
# Content-Type: application/x-www-form-urlencoded
# -----
# username=admin&password=admin
@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        for i in request.form:
            print "DM: request.form[%s] = [%s]" % (i, request.form[i])
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username']), 301
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)


# /login/admin?password=admin
@app.route("/login/<username>", methods=["POST", "GET"])
def login_user(username):
    error = None
    if request.method == "POST":
        for i in request.args:
            print "DM: request.args.get(%s) = [%s]" % (i, request.args.get(i, ''))
        password_from_url = request.args.get('password', '')
        if valid_login(username, password_from_url):
            return log_the_user_in(username), 301
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)



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
