#!/usr/bin/env python
# http://flask.pocoo.org/docs/0.11/quickstart/

from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import hashlib

app = Flask(__name__)

CONST_PATH_UPLOAD_FOLDER = "storage\\uploads"
app.config["UPLOAD_FOLDER"] = CONST_PATH_UPLOAD_FOLDER

FIG_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif")
DOC_EXTENSIONS = (".txt", ".pdf", ".doc", ".docx")


# =====
# route() decorator is used to bind a function to a URL.
# =====

@app.route("/")
def root():
    return "index page"


def is_supported_filetype_by_ext_name(filename):
    ext_name = os.path.splitext(filename)[-1].lower()
    if ext_name:
        if ext_name in FIG_EXTENSIONS or \
                        ext_name in DOC_EXTENSIONS:
            return True
    return False


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # assert file should be part of request.files
        if "file" not in request.files:
            print "ERROR: No file part"
            return redirect(request.url)
        file = request.files["file"]
        if len(file.filename) == 0:
            print "WARNING: user not selected files"
            return redirect(request.url)
        if file and is_supported_filetype_by_ext_name(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print "DM: saving {} ...".format(file.filename)
            new_name = _rename_by_sha1(app.config["UPLOAD_FOLDER"], filename)
            return redirect(url_for("uploaded_file", filename=new_name))
        else:
            print "DM: {} not acceptable".format(file.filename)
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def _rename_by_sha1(path_folder, filename):
    ext = os.path.splitext(filename)[1].lower()
    sha1 = hashlib.sha1()
    old_file = os.path.join(path_folder, filename)
    # calculate sha1 value on file content
    with open(old_file, "rb") as reader:
        while True:
            data = reader.read(1024*64)
            if not data:
                break
            sha1.update(data)
    # in filesystem, file rename or purge if identical file exists
    new_filename = "".join([sha1.hexdigest(), ext])
    new_file = os.path.join(path_folder, new_filename)
    print "DM: {} -> {}".format(old_file, new_file)
    try:
        os.rename(old_file, new_file)
    except WindowsError as err: # file
        print "ERROR: " + str(err)
        print "DM: os.remove({})".format(old_file)
        os.remove(old_file)
    return new_filename


# [windows]
# set FLASK_APP=flask_hello.py
# set FLASK_DEBUG=1
# [linux]
# export FLASK_APP=flask_hello.py
# export FLASK_DEBUG=1
# python -m flask run
# python -m flask run --host=0.0.0.0 --port=8080

if __name__ == '__main__':
    if not os.path.exists(CONST_PATH_UPLOAD_FOLDER):
        os.makedirs(CONST_PATH_UPLOAD_FOLDER)
    app.run(debug=True)
