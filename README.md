# Final_Project
CS50 Final Project

My name is Renata Barcelos from Brazil and this is my CS50's Final Project: "New's Collection"

I've developed a website built upon the data and functionality of an existing application called Bing News Search API. 

Listed below are the web technologies I used in this project:

. HTML
. CSS
. JavaScript
. Python
. API - application programming interface
. JSON
. SQLite
. Flask
. BootStrap
. Jinja

The website displays a list of the latest news articles published worldwide according to users search parameters such as **Language** and **articles topics** 
like "health, election, university and any others". 

To mannage those API requests I used a API Hub called RapidAPI which helps developers find and connect to tens of thousands of public APIs across multiple cloud 
environments. 

As the user gets access to the **Index** page he will be able to choose his Language and topic preferences and click the Search button that will redirect him to a 
second page called **News** that will display in grid formatting all the latest news given as response from the Bing API request related to user's search query string
ordered by publication date. 
This page will also advise the user by a Flash message to sign up and Login to have access to features like saving or sharing favorites articles. 

The **Register** and **Login** pages use Flask forms and JavaScript functions to validate and store input from user such as username and password. As the criteria for
each of them is met the user will be logged in by Flask-Login (which provides user session management) and redirected to his own personalized private page where he 
will be able to see and filter his favorites articles that can now be saved and shared from **News** page. 
The *share* button allows user to email the news URL.
