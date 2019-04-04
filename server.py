from flask import Flask, render_template, request, redirect
import os
from collections import namedtuple, defaultdict

app = Flask(__name__)

User = namedtuple("User", "password")
Moderator = namedtuple("Moderator","password")
users = defaultdict()
moderators = defaultdict()
ambulances = defaultdict()
# dummy data
moderators["rishabhkalakoti@gmail.com"]=Moderator(password = "letmepass")
users["8440949302"]=User(password = "letmepass")


@app.errorhandler(404)
def error404(error):
    return redirect("/")

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verifyMod", methods=["POST"])
def verifyMod():
	user_id = request.form["email"]
	pwd = request.form["pwd"]
	if(user_id in moderators):
		if(moderators[user_id].password == pwd):
			#todo: create session
			return redirect("/dashboard")
	return "Incorrect username/password"

@app.route("/verifyUser", methods=["POST"])
def verifyUser():
	user_id = request.form["user_id"]
	pwd = request.form["pwd"]
	if(user_id in moderators):
		if(moderators[user_id].password == pwd):
			# todo: create session
			return redirect("/booking")
	return "Incorrect username/password"

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/logout")
def logout():
	# todo- destroy session
	return render_template("login.html")


@app.route("/static/<path:path>")
def server_static(path):
    return app.send_static_file("static/" + path)

app.run(host="localhost", port=8080)
