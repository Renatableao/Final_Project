import sqlite3
from ssl import VERIFY_X509_PARTIAL_CHAIN
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_mail import Mail, Message
from time import time
import jwt
import os
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv, find_dotenv
from helpers import login_required, search
# Configure application
app = Flask(__name__)

# Configure Flask_mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('email_username')
app.config['MAIL_PASSWORD'] = os.environ.get('email_key')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)

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

		# User clicks favorite button to save article
		if request.form.get("favorite"):
			news_data = db.execute("SELECT * FROM news WHERE name = ?", [request.form.get("favorite")])
			new_data = news_data.fetchall()
			
			# Save article in database with user_id
			db.execute("INSERT INTO user_news(user_id, category, name, url, description, provider, date) SELECT ?, ?, ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM user_news WHERE name = ? AND user_id = ?)", [session.get("user_id"), new_data[0][1], new_data[0][2], new_data[0][3], new_data[0][4], new_data[0][5], new_data[0][6], new_data[0][2], session.get("user_id")])
			con.commit()
			return ('', 204)

		else: 
			# Ensure language is provided
			if request.form.get("input_language") == "language":
				flash("Please select language!")
				return redirect("/")
		
			# Ensure category topic is provided
			if not request.form.get("input_category"):
				flash("Please type in a search topic!")
				return redirect("/")

			# Call API results with given parameters 
			else:	
				country = request.form.get("input_language")
				category = request.form.get("input_category")

				news_result = search(country, category)
			
				#If results equal none
				if not news_result:
					flash("No results on this topic. Try anther one!")
					return redirect("/")
			
				#If valid results
				else:
					for new in news_result: 
						# Save searched articles in "news" database to be used in signed in session
						db.execute("INSERT OR IGNORE INTO news(category, name, url, description, provider, date) VALUES (?, ?, ?, ?, ?, ?)", [category, new['name'], new['url'], new['description'],new['provider'][0]['name'], new['datePublished']])
						con.commit()

					# Advise user
					if not session.get("user_id"):
						flash("Sign in to save or share your favorite news!")

					return render_template("news.html", news_result=news_result, category=category)

	# User reached route via GET
	else:
		return render_template("index.html")
	

@app.route("/mylist", methods=["GET", "POST"])
@login_required
def my_list():
	
	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":
		
		# User deletss article from favorites
		if request.form.get("delete"):
			db.execute("DELETE FROM user_news WHERE name = ? AND user_id = ?", [request.form.get("delete"), session.get("user_id")])
			con.commit()
			return redirect("/mylist")

		
		else:
			# Ensure language is provided
			if request.form.get("input_filter") == "filter":
				flash("Please select category!")
				return redirect("/mylist")

			else:
				# Get input from user for filtered category
				filter_category = request.form.get("input_filter")

				# Query database for users news list categories
				my_news_categories = db.execute("SELECT DISTINCT category FROM user_news WHERE user_id = ?", [session.get("user_id")])
				my_categories = my_news_categories.fetchall()

				# Query database for users news list
				my_category_filter = db.execute("SELECT * FROM user_news WHERE user_id = ? AND category = ?", [session.get("user_id"), filter_category])
				my_category = my_category_filter.fetchall()
		
			return render_template("my_list_filtered.html", my_categories=my_categories, my_category=my_category, filter_category=filter_category)
	
	else:

		# Query database for users news list
		user_list = db.execute("SELECT * FROM user_news WHERE user_id = ?", [session.get("user_id")])
		user_news = user_list.fetchall()

		# Query database for users news list categories
		my_category = db.execute("SELECT DISTINCT category FROM user_news WHERE user_id = ?", [session.get("user_id")])
		my_categories = my_category.fetchall()

		return render_template("my_list.html", user_news=user_news, my_categories=my_categories)


@app.route("/register", methods=["GET", "POST"])
def register():
	"""Register user"""
	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":

			# Query database for username
			user = db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
			user_l = user.fetchall()

			# Ensure username is not already used
			if len(user_l) == 1:
				flash("User already exists! Please register another one.")
				return render_template("register.html")

			hash = generate_password_hash(request.form.get("password"))

			db.execute("INSERT INTO users(username, email, hash) VALUES (?, ?, ?)", [(request.form.get("username")) , (request.form.get("email")), hash])
			con.commit()

			# Remember which user has logged in
			user = db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
			user_l = user.fetchall()
			session["user_id"] = user_l[0][0]
			session["user_username"] = user_l[0][1]

			# Redirect user to favorites
			flash("Registered!")
			return redirect("/mylist")

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


		# Query database for user
		user = db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
		user_l = user.fetchall()

		# Ensure email exists and password is correct
		if len(user_l) != 1 or not check_password_hash(user_l[0][2], request.form.get("password")):
			flash("Invalid email and/or password!")
			return render_template("login.html")

		# Remember which user has logged in
		session["user_id"] = user_l[0][0]
		session["user_username"] = user_l[0][1]

		# Redirect user to favorites
		return redirect("/mylist")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("login.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
	
	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":

		# Query database for user
		user_input = db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])
		user_l = user_input.fetchall()
		user = user_l[0][0]

		# Ensure email is already registered
		if len(user_l) != 1:
			flash("Not a registered email!")
			return render_template("forgot_password.html")
		
		# Generate reset token
		load_dotenv(find_dotenv())
		key = os.environ.get('SECRET_KEY')
		token = jwt.encode({"reset": user_l[0][3], 'exp': time() + 120}, key, algorithm="HS256")
		
		#Save token in database
		db.execute("UPDATE users SET token = ? WHERE id = ?", [token, user])
		con.commit()

		#Send email with reset link
		msg = Message('Password reset request', sender = os.environ.get('email_username'), recipients = [user_l[0][3]])
		msg.body = f"To reset your password, please follow the link bellow. {url_for('reset_password', token=token, user=user, _external=True)}"
		mail.send(msg)
		flash("Verification link sent. Please check your email.")
		return redirect("/forgot_password")

	else:
		return render_template("forgot_password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

	user = request.args.get('user')
	token = request.args.get('token')

	if request.method == "POST":

		hash = generate_password_hash(request.form.get("password"))
		db.execute("UPDATE users SET hash = ? WHERE id = ?", [hash, request.form.get("user")] )
		con.commit()
		flash("Password reset successfully!")
		return redirect('/login')
		
		
	else:
		load_dotenv(find_dotenv())
		key = os.environ.get('SECRET_KEY')
		try:
			jwt.decode(token, key, algorithms="HS256")
			user_token = db.execute("SELECT token FROM users where id= ?", [user]).fetchall()[0][0]
			if token == user_token:
				db.execute("UPDATE users SET token = ?  WHERE id = ?", ["", user])
				con.commit()
				return render_template("reset_password.html", user=user)
			else:
				flash("Invalid link! Please request a new one.")
				return redirect("/forgot_password")
		except jwt.ExpiredSignatureError:
			flash("Token has expired! Please request a new one.")
			db.execute("UPDATE users SET token = ?  WHERE id = ?", ["", user])
			con.commit()
			return redirect("/forgot_password")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

		if request.method == "POST":
			hash = generate_password_hash(request.form.get("password"))
			db.execute("UPDATE users SET hash = ? WHERE id = ?", [hash, session.get("user_id")] )
			con.commit()
			flash("Password changed successfully!")
			return redirect('/change_password')

		else:
			return render_template("change_password.html")

@app.route("/logout")
def logout():
	"""Log user out"""

	# Forget any user_id
	session.clear()

	# Redirect user to login form
	return redirect("/")
