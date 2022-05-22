import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, redirect, render_template, request, session
from functools import wraps


def search(country, category):
	# Contact API
	load_dotenv(find_dotenv())
	try:
		
		url = "https://bing-news-search1.p.rapidapi.com/news/search"

		querystring = {"q": category, "count":"27", "sortBy":"date","cc": country,"freshness":"Month","originalImg":"true","textFormat":"Raw","safeSearch":"Strict"}

		headers = {
				"X-BingApis-SDK": "true",
				"Accept-Language": "portuguese;english;french;italian;chinese",
				"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
				"X-RapidAPI-Key": os.environ.get('API_key')
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

	
