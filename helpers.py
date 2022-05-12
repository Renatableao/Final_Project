import os
import requests

from flask import redirect, render_template, request, session
from functools import wraps

def search(country, category):
    # Contact API
	try:
		url = "https://bing-news-search1.p.rapidapi.com/news"
		querystring = {"category": category, "cc": country ,"safeSearch":"Off","textFormat":"Raw"}

		headers = {
			"Accept-Language": "english;portuguese;french;chinese;italian",
			"X-BingApis-SDK": "true",
			"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
			"X-RapidAPI-Key": "cdb8c2abdbmsha2aaa1234be25eap1bb3b8jsnf76ce06b28fb"
		}

		response = requests.request("GET", url, headers=headers, params=querystring)

	except requests.RequestException:

		return None

	# Parse response
	try:
		result = response.json()
		news = result["value"]
		return news
		
        
	except (KeyError, TypeError, ValueError):
		return None


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function