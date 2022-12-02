import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from cs50_helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select cash user has left to spend
    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]
    # This will be added to in a for loop with values of total prices of shares owned. This should eventually add up to ~10000
    total = cash 

    # Select symbol and sum of shares for each symbol
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", 
                        session["user_id"])

    # For each row in stocks
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total_price"] = stock["price"] * stock["shares"]
        total += stock["total_price"]

    return render_template("index.html", cash=cash, total=total, stocks=stocks)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # lookup stock symbol
        stocksymbol = request.form.get("symbol")
        if not stocksymbol:
            return apology("Missing stock symbol")

        quote = lookup(stocksymbol)
        if quote is None:
            return apology("Invalid stock symbol")

        shares = request.form.get("shares")
        if not shares:
            return apology("Missing shares input")
        if shares.isdigit() == False or int(shares) < 0:
            return apology("The number of shares is not a positive integer")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_avail = cash[0]["cash"]

        total_price = int(shares) * quote["price"]

        if total_price > cash_avail:
            return apology("You cannot afford the number of shares of this stock at its current price")

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", 
                   session["user_id"], stocksymbol, shares, quote["price"])

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_price, session["user_id"])

        # Redirect user to index
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # lookup stock symbol
        stocksymbol = request.form.get("symbol")
        if not stocksymbol:
            return apology("Stock symbol has not been inputted.")

        quote = lookup(stocksymbol)
        if quote is None:
            return apology("Stock symbol doesn't exist.")

        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("Username already exists", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        # Insert input into table of users
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", 
                         session["user_id"])
    symbols_list = []
    for index in range(len(symbols)):
        for key in symbols[index]:
            symbols_list.append(symbols[index][key])

    if request.method == "POST":
        # lookup stock symbol
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        shares = request.form.get("shares")
        rows = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", 
                          session["user_id"], symbol)

        if symbol not in symbols_list:
            return apology("You did not select a stock")
        if not shares:
            return apology("You did not input an amount for shares")
        if len(rows) != 1:
            return apology("You do not own any shares of this stock")
        if shares.isdigit() == False or int(shares) < 0:
            return apology("Shares should be a positive integer")
        if int(shares) > rows[0]["shares"]:
            return apology("Too many shares selected")

        total_price = int(shares) * quote["price"]

        db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", 
                   session["user_id"], symbol, -int(shares), quote["price"])
        # update cash in users
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_price, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", symbols=symbols_list)


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    """Reset password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not password or not confirm:
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Please input a new password")

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(password), session["user_id"])
        return redirect("/")

    else:
        return render_template("resetpassword.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
