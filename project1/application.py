import os, requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from xml.etree import ElementTree as ET

# in case you forget $env:FLASK_APP ='application.py'
#                    $env:FLASK_ENV ='development'
#                     $env:DATABASE_URL ='postgres://tdhdggnfxoibqd:7fa5ac7a5fa982df20bed4657453282ea70117c16183913330fad915db0388e6@ec2-54-247-96-169.eu-west-1.compute.amazonaws.com:5432/d8qhuaikilqost'

app = Flask(__name__)
reviews = []
ratings = []
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    else:
        username = request.form.get("new_username")
        password = request.form.get("new_password")
        if checkUser(username) == None:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
            db.commit()
            return render_template("index.html", message = "User Registered")
        else:
            return render_template("error.html", message = "username already exists")

@app.route("/user", methods = ["POST"])
def user():
    username = request.form.get("username")
    password = request.form.get("password")
    if checkUser(username) == None:
        return render_template("error.html", message = "username does not exist")

    elif checkAccount(username, password):
        return render_template("profile.html",name = username )

    #handle login details
    return render_template("error.html", message = "invalid login details")


@app.route("/login", methods = ["GET"])
def login():
    return render_template("login.html")

@app.route("/search", methods = ["GET","POST"])
def search():
    if session.get("books") == None:
        session["books"] = []
    elif request.method == 'GET':
        session["books"] = []

    elif request.method == 'POST':
        info = request.form.get("info")
        results = userResult(info)
        session["books"] = results

    return render_template("search.html", books = session["books"])


@app.route("/book/<string:id>", methods = ["GET","POST"])
def book(id):
    if request.method == "POST":
        review = request.form.get("review")
        rating = request.form.get("rating")
        ratings.append(rating)
        reviews.append(review)

    session["book"] = bookResult(id)
    return render_template("book.html", book = session["book"], reviews = reviews, ratings = ratings)

#Function Used

def checkUser(name):

    data =  db.execute("SELECT username FROM users WHERE username = :username", {"username": name}).fetchone()
    return data


def checkAccount(name,password):
    data =  db.execute("SELECT username FROM users WHERE username = :username AND password = :password", {"username": name, "password":password}).fetchone()
    return data

def userResult(query):
    res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "mfCKZwz2EpuiaQl8NYktmQ", "q": query})
    root = ET.fromstring(res.content)
    list = []
    for child in root[1][6]:
        details = {}
        details["title"] = child[8][1].text
        details["author"] = child[8][2][1].text
        details["id"] = child[8][0].text
        list.append(details)
    return list

def bookResult(id):
    res = requests.get("https://www.goodreads.com/book/show.xml", params = {"key": "mfCKZwz2EpuiaQl8NYktmQ", "id": id})
    root = ET.fromstring(res.content)
    details = {}
    details["title"] = root[1][1].text
    details["description"] = root[1][16].text
    details["author"] = root[1][26][0][1].text
    details["year"] = root[1][10].text
    details["rating"] = root[1][18].text
    details["id"] = root[1][0].text
    return details
