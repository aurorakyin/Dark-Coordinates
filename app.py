import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
# from helpers import requests

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///user.db")


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
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords no matchey")

        # Remember which user has logged in
        try:
            rows = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("username taken")

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
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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
    return render_template("mentalhaven.html", rows=rows)


@app.route("/avoid", methods=["GET", "POST"])
def avoid():
    """how to avoid contact with ghosts"""
    return render_template("avoid.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """how to get in contact with ghosts"""
    return render_template("contact.html")


@app.route("/me", methods=["GET", "POST"])
def me():
    """profile page"""
    return render_template("me.html")

@app.route("/bloodymary", methods=["GET", "POST"])
def bloodymary():
    """bloody mary"""
    return render_template("bloodymary.html")
'''
def favorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = session["userid"] AND favorite = 'bloodymary'")
    # Ensure username exists and password is correct
    if len(rows) != 0
       return render_template("bloodymary.html")
    
    rows = db.execute("INSERT INTO favorites (userid, favorite) VALUES (?, ?)", session["userid"], bloodymary)
    return render_template("bloodymary.html")

def unfavorite():
    rows = db.execute("SELECT * FROM favorites WHERE userid = session["userid"] AND favorite = 'bloodymary'")
    # Ensure username exists and password is correct
    if len(rows) != 1
       return render_template("bloodymary.html")
    
    rows = db.execute("DELETE FROM favorites WHERE userid = session ["userid"] AND favorite = 'bloodymary'")
    return render_template("bloodymary.html")
'''