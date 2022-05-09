import re
import sqlite3
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import search, apology
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite to read database
con = sqlite3.connect("finalproject.db", check_same_thread=False)
db = con.cursor()

@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response


@app.route("/", methods=["GET", "POST"])
def index():
	
	# User reached route via POST
	if request.method == "POST":
	
		# Ensure symbol is provided
		if not request.form.get("language"):
			return apology("Must provide language", 400)

		if not request.form.get("category"):
			return apology("Must provide category", 400)

		else:	
			language = request.form.get("language")
			category = request.form.get("category")
		
			result = search(language, category)

			return render_template("news.html", result=result)


	# User reached route via GET
	else:
		return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 400)

        # Ennsure username has at least 3 characters and not only numbers
        elif len(request.form.get("username")) < 3 or re.match('[0-9]', request.form.get("username")):
            return apology("Must provide valid username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 400)

        # Ensure password has at least 6 characters and contain lowercase letters, numbers and special characters
        elif re.match('^(.{0,5}|[^0-9]*|[^a-z]*|[a-zA-Z0-9]*)$', request.form.get("password")):
            return apology("Must provide valid password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Must confirm password", 400)

        # Ensure password confirmation is the same as password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords do not match", 400)

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        user_l = user.fetchall()

        # Ensure username is not already used
        if len(user_l) == 1:
            return apology("Username already in use", 400)

        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", [(request.form.get("username")) , hash])
        con.commit()

        # Remember which user has logged in
        user = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        user_l = user.fetchall()
        session["user_id"] = user_l[0][0]

        # Redirect user to home page
        flash("Registered!")
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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        user_l = user.fetchall()

        # Ensure username exists and password is correct
        if len(user_l) != 1 or not check_password_hash(user_l[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user_l[0][0]

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
