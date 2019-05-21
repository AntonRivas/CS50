from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/", methods = ["GET","POST"])

def index():
    if session.get("notes") == None:
        session["notes"] = []

    elif request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)

    return render_template("index.html", notes = session["notes"])

@app.route("/more" , methods = ["POST"] )

def more():
    name = request.form.get("name")

    return render_template("more.html", name = name)

@app.route("/<string:name>")

def nameSearch(name):

    return f"hello {name}"
