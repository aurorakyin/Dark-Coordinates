import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///darkcoor.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Homepage with navbar and world map etc"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("register.html")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("must confirm password")
            return render_template("register.html")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html")

        # Remember which user has logged in
        try:
            rows = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))
        except:
            flash("username taken")
            return render_template("register.html")

        session["user_id"] = rows

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("register.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return render_template("register.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("login.html")


@app.route("/directory")
def directory():
    """Directory of ghosts and urban legends"""
    return render_template("directory.html")


@app.route("/mentalhaven")
def mentalhaven():
    """Show mental haven with cute videos"""
    return render_template("mentalhaven.html")


@app.route("/avoid")
def avoid():
    """how to avoid contact with ghosts"""
    return render_template("avoid.html")


@app.route("/contact")
def contact():
    """how to get in contact with ghosts"""
    return render_template("contact.html")


@app.route("/me", methods=["GET", "POST"])
def me():
    """profile page"""
    user_id = session["user_id"]

    likedstories = db.execute(
        "SELECT favorite AS likedstory FROM favorites WHERE userid = ?", user_id)

    return render_template("me.html", likedstories=likedstories)

@app.route("/bloodymary", methods=["GET", "POST"])
def bloodymary():
    """bloody mary"""
    return render_template("bloodymary.html")

def favorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], bloodymary)
    # Ensure username exists and password is correct
    if len(rows) != 0:
       return render_template("bloodymary.html")

    rows = db.execute("INSERT INTO favorites (userid, favorite) VALUES (?, ?)", session["user_id"], bloodymary)
    return render_template("bloodymary.html")

def unfavorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], bloodymary)
    # Ensure username exists and password is correct
    if len(rows) != 1:
       return render_template("bloodymary.html")

    rows = db.execute("DELETE FROM favorites WHERE userid = ? AND favorite = ?", session["userid"], bloodymary)
    return render_template("bloodymary.html")

@app.route("/tokoloshe", methods=["GET", "POST"])
def tokoloshe():
    """tokoloshe"""
    return render_template("bloodymary.html")

def favorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], tokoloshe)
    # Ensure username exists and password is correct
    if len(rows) != 0:
       return render_template("bloodymary.html")

    rows = db.execute("INSERT INTO favorites (userid, favorite) VALUES (?, ?)", session["user_id"], tokoloshe)
    return render_template("tokoloshe.html")

def unfavorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], tokoloshe)
    # Ensure username exists and password is correct
    if len(rows) != 1:
       return render_template("tokoloshe.html")

    rows = db.execute("DELETE FROM favorites WHERE userid = ? AND favorite = ?", session["userid"], tokoloshe)
    return render_template("tokoloshe.html")

@app.route("/waverlyhills", methods=["GET", "POST"])
def waverlyhills():
    """waverlyhills"""
    return render_template("waverlyhills.html")

def favorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], waverlyhills)
    # Ensure username exists and password is correct
    if len(rows) != 0:
       return render_template("waverlyhills.html")

    rows = db.execute("INSERT INTO favorites (userid, favorite) VALUES (?, ?)", session["user_id"], waverlyhills)
    return render_template("waverlyhills.html")

def unfavorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], waverlyhills)
    # Ensure username exists and password is correct
    if len(rows) != 1:
       return render_template("waverlyhills.html")

    rows = db.execute("DELETE FROM favorites WHERE userid = ? AND favorite = ?", session["userid"], waverlyhills)
    return render_template("waverlyhills.html")

@app.route("/yamamurasadako", methods=["GET", "POST"])
def yamamurasadako():
    """yamamurasadako"""
    return render_template("yamamurasadako.html")

def favorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], yamamurasadako)
    # Ensure username exists and password is correct
    if len(rows) != 0:
       return render_template("yamamurasadako.html")

    rows = db.execute("INSERT INTO favorites (userid, favorite) VALUES (?, ?)", session["user_id"], yamamurasadako)
    return render_template("yamamurasadako.html")

def unfavorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = ? AND favorite = ?", session["user_id"], yamamurasadako)
    # Ensure username exists and password is correct
    if len(rows) != 1:
       return render_template("yamamurasadako.html")

    rows = db.execute("DELETE FROM favorites WHERE userid = ? AND favorite = ?", session["userid"], yamamurasadako)
    return render_template("yamamurasadako.html")
