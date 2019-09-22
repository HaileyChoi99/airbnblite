# AirBnBLiteProject
# airbnblite project for hack4impact
from flask import Flask, Response, Request
from flask_pymongo import pymongo
from flask import render_template
from database  import DatabaseConnection
from UserService import UserService

import datetime
import uuid

app = Flask(__name__)
app.secret_key = "airbnblite"
db = DatabaseConnection()
userService = UserService()


@app.route("/addNewProperty", methods=["GET"])
def getPropertyForm():
    return render_template("addNewProperty.html")

@app.route("/addNewProperty", methods=["POST"])
def addNewProperty():
    document = {
        name: request.form["name"],
        propertyType: request.form["type"],
        price: request.form["price"]
    }
    db.insert("properties", document)
    return Response("Property successfully added", status=200, content_type="text/html")

@app.route("/properties", methods=["GET"])
def getProperties():
    properties = db.findMany("properties", {})
    return render_template("properties.html", properties=properties)

@app.route("/", methods=["GET"])
def heythere():
    return Response("<h1> Hey there </h1>", status=200, content_type="text/html")


@app.route("/greeting", methods=["POST"])
def greeting():
    name = request.form["name"]
    hourOfDay = datetime.datetime.time().hour
    greeting = ""
    if not name:
        return Response(status=404)
    if hourOfDay < 12:
        greeting = "Good Morning"
    elif hourOfDay > 12 and hourOfDay < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    response = greeting + " " + name + "!"
    return Response(response, status=200, content_type="text/html")

@app.route("/login", methods=["GET"])
def getLoginView():
    if request.cookies.get("sid"):
        return render_template("welcome.html")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if userService.authenticate(username, password):
        response = make_response(render_template("welcome.html"))
        sid = str(uuid.uuid4())
        session = {
            "sid": sid,
            "username": username
        }
        db.insert("sessions", session)
        response.set_cookie("sid", sid)
        return response
    else:
        flash("Incorrect login credentials")
        return render_template("login.html")

    return render_template("account.html", firstName=firstName)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
