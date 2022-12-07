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
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    usertransactions = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    userscash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = userscash[0]["cash"]
    totall = db.execute("SELECT SUM(purchasevalue) AS purchasevalue FROM transactions WHERE user_id = ?", user_id)
    total = totall[0]["purchasevalue"]
    if total is None:
        total = cash
    else:
        total += cash

    holdings = []
    for row in usertransactions:
        quote = lookup(row["symbol"])
        value = (quote["price"] * row["shares"])
        holdings.append({"symbol": quote["symbol"], "name": quote["name"], "shares": row["shares"],
                        "price": usd(quote["price"]), "value": usd(value)})

    return render_template("index.html", holdings=holdings, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("your input of symbol is a must")

        # Ensure symbol is valid
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol ;-;")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("use positive integer for share(s) plz")

        if shares <= 0:
            return apology("use positive integer for share(s) plz")

        value = int(request.form.get("shares")) * quote["price"]
        user_id = session["user_id"]
        users_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = users_cash[0]["cash"]

        if user_cash < value:
            return apology("need more money")

        # Update user cash
        user_newcash = user_cash - value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_newcash, user_id)

        # Insert transaction into transactions
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, purchasevalue) VALUES (?, ?, ?, ?, ?)", user_id,
                   quote["symbol"], request.form.get("shares"), quote["price"], int(request.form.get("shares"))*quote["price"])

        flash("Successfully bought :)")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, time FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", rows=rows)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")

        # Ensure symbol is submitted
        if not symbol:
            return apology("your input of symbol is a must")

        # Ensure symbol is valid
        quote = lookup(symbol)

        if quote == None:
            return apology("invalid symbol ;-;")

        # Get quote accordingly
        return render_template("quoted.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])

    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        usersymbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ?  GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in usersymbols])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure symbol is submitted
        if not symbol:
            return apology("your input of symbol is a must")

        # Ensure symbol is valid
        quote = lookup(symbol)

        if quote == None:
            return apology("invalid symbol ;-;")

        # Ensure shares is positive integer
        if shares <= 0 or not isinstance(shares, int):
            return apology("positive integer for share(s) plz")

        value = shares * quote["price"]
        user_id = session["user_id"]
        users_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = users_cash[0]["cash"]
        users_shares = db.execute(
            "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        user_shares = users_shares[0]["shares"]

        if shares > user_shares:
            return apology("not enough shares")

        # Update user cash
        user_newcash = user_cash + value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_newcash, user_id)

        # Insert transaction into transactions
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, purchasevalue) VALUES (?, ?, ?, ?, ?)",
                   user_id, quote["symbol"], -shares, quote["price"], -shares*quote["price"])

        flash("Sold :)")

        # Redirect user to home page
        return redirect("/")


@app.route("/bank", methods=["GET", "POST"])
@login_required
def bank():
    """Add or take out money"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        amount = request.form.get("amount")

        # Ensure symbol is submitted
        if not amount:
            return apology("your input of amount is a must")

        user_id = session["user_id"]
        users_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = users_cash[0]["cash"]

        # Update user cash
        user_newcash = user_cash + float(amount)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_newcash, user_id)

        flash("Cash Amount Updated :)")

        return redirect("/")

    else:
        return render_template("bank.html")
