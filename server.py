from flask import Flask, render_template, request, redirect, session
import os
import random
import string
from collections import namedtuple, defaultdict

app = Flask(__name__)

User = namedtuple("User", "password booking")
Moderator = namedtuple("Moderator","password")
Ambulance = namedtuple("Ambulance","driver phone is_booked")
users = defaultdict()
moderators = defaultdict()
ambulances = defaultdict()

def addAmbulance(Driver, Phone):
	ambulance_id = None
	while True:
		r = ''.join(
			[random.choice(string.ascii_letters + string.digits) 
			for n in range(10)]
			)
		if(r not in ambulances):
			ambulance_id = r
			break
	ambulances[r] = Ambulance(driver=Driver, phone=Phone,is_booked=False)

@app.route("/add", methods=["POST"])
def add():
	if not (session.get("logged_in")=="mod"):
		return render_template("login.html")
	driver = request.form["driver"]
	phone = request.form["phone"]
	addAmbulance(driver,phone)
	return redirect("/dashboard")

@app.route("/remove/<amb_id>")
def remove(amb_id):
	if not (session.get("logged_in")=="mod"):
		return render_template("login.html")
	ambulances.pop(amb_id)
	return redirect("/dashboard")

@app.route("/modify", methods=["POST"])
def modify():
	if not (session.get("logged_in")=="mod"):
		return render_template("login.html")
	driver = request.form["driver"]
	phone = request.form["phone"]
	amb_id = request.form["amb_id"]
	ambulances[amb_id] = ambulances[amb_id]._replace(
		driver = driver, phone = phone)
	return redirect("/dashboard")

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
			session["logged_in"] = "mod"
			session["user_id"] = user_id
			return redirect("/dashboard")
	return "Incorrect username/password"

@app.route("/verifyUser", methods=["POST"])
def verifyUser():
	user_id = request.form["user_id"]
	pwd = request.form["pwd"]
	if(user_id in users):
		if(users[user_id].password == pwd):
			session["logged_in"] = "user"
			session["user_id"] = user_id
			return redirect("/booking")
	return "Incorrect username/password"

@app.route("/dashboard")
def dashboard():
	if not (session.get("logged_in")=="mod"):
		return render_template("login.html")
	ambulances_data = [
			(amb_id, amb_info.driver, amb_info.phone, amb_info.is_booked)
			for amb_id, amb_info in ambulances.items()
		]
	return render_template("dashboard.html", ambulances = ambulances_data)

@app.route("/book/<book_id>")
def book(book_id):
	if not (session.get("logged_in")=="user"):
		return render_template("login.html")
	users[session.get("user_id")] = users[session.get("user_id")]._replace(
		booking = book_id)
	ambulances[book_id] = ambulances[book_id]._replace(
		is_booked = session.get("user_id"))
	return redirect("/booking")

@app.route("/cancelBooking")
def cancelBooking():
	if not (session.get("logged_in")=="user"):
		return render_template("login.html")
	book_id = users[session.get("user_id")].booking
	users[session.get("user_id")] = users[session.get("user_id")]._replace(
		booking = None)
	ambulances[book_id] = ambulances[book_id]._replace(is_booked = False)
	return redirect("/booking")

@app.route("/booking")
def booking():
	if not (session.get("logged_in")=="user"):
		return render_template("login.html")
	free_ambulances = [
			(amb_id, amb_info.driver, amb_info.phone, amb_info.is_booked)
			for amb_id, amb_info in ambulances.items()
		]
	booking = users[session.get("user_id")].booking
	if booking!=None:
		booking = ambulances[booking]
	return render_template("booking.html", 
		ambulances = free_ambulances, booking = booking)

@app.route("/logout")
def logout():
	session["logged_in"]=False
	session["user_id"]=None
	return render_template("login.html")


@app.route("/static/<path:path>")
def server_static(path):
    return app.send_static_file("static/" + path)


# dummy data
moderators["rishabhkalakoti@gmail.com"]=Moderator(password = "letmepass")
users["8440949302"]=User(password = "letmepass", booking=None)
addAmbulance("DummyDriver1",9627910025)
addAmbulance("DummyDriver2",1234567890)


app.secret_key = os.urandom(12)
app.run(host="localhost", port=8080)
