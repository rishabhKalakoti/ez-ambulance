from bottle import Bottle, run, template, static_file, request, route, redirect, error
import os
from collections import namedtuple, defaultdict

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
app = Bottle()

User = namedtuple("User", "password")
Moderator = namedtuple("Moderator","password")
users = defaultdict()
moderators = defaultdict()
ambulances = defaultdict()
# dummy accounts
moderators["rishabhkalakoti@gmail.com"]=Moderator(password = "letmepass")
users["8440949302"]=User(password = "letmepass")

@app.route("/")
def changePath():
    return template("templates/login.html")

@error(404)
def error404(error):
    return redirect("/")

@app.get("/login")
def login():
    return template("templates/login.html")

@app.post("/verifyMod")
def verifyMod():
	user_id = request.forms.get("email")
	pwd = request.forms.get("pwd")
	if(user_id in moderators):
		if(moderators[user_id].password == pwd):
			return "Logged in"
	return "Incorrect username/password"

@app.post("/verifyUser")	
def verifyUser():
	user_id = request.forms.get("user_id")
	pwd = request.forms.get("pwd")
	if(user_id in moderators):
		if(moderators[user_id].password == pwd):
			return "Logged in"
	return "Incorrect username/password"

@app.get("/dashboard")
def dashboard():
	return "dash"

@app.get("/booking")
def booking():
	return "book"

@app.get("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=os.path.join(dir_path, "static"))

run(app, host="localhost", port=8080)
