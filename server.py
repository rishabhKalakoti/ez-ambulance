from bottle import Bottle, run, template, static_file, request, route, redirect, error
import os
from collections import namedtuple

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
app = Bottle()

users = namedtuple("user","password")
moderator = namedtuple("moderator","password")

@app.route("/")
def changePath():
    return template("templates/login.html")

@error(404)
def error404(error):
    return redirect("/")

@app.get("/login")
def download():
    return template("templates/login.html")

@app.get("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=os.path.join(dir_path, "static"))

run(app, host="localhost", port=8080)
