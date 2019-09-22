from flask import Flask, Response, Request
from flask_pymongo import pymongo
from pymongo import MongoClient
from flask import render_template


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SomeDatabase"
app.config['MONGO_DBNAME'] = 'SomeCollection'
app.config['SECRET_KEY'] = 'secret_key'
pymongo = pymongo(app)


mongo = pymongo(app)
db = mongo.db
col = mongo.db["Some Collection"]
print ("MongoDB Database:", mongo.db)

@app.route("/")
def home_page():
    online_users = mongo.db.users.find({"online": True})
    return render_template("hello.html",
        online_users=online_users)

@app.route("/")
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)