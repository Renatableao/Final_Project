# Final_Project
CS50 Final Project

CS50 Final Project

My name is Renata Barcelos. I'm from Brazil and this is my CS50's Final Project: "New's Collection".

I've developed a responsive website built upon the data and functionality of an existing application called Bing News Search API.

Listed below are the web technologies I used in this project:

. HTML . CSS . JavaScript . Python . API (application programming interface) . JSON . SQLite . Flask . Flask-mail . BootStrap . Jinja 

The website displays a list of the latest news articles published worldwide according to users search parameters such as Language and articles topics like "health, election, university and many others".

To mannage the Bing News Sarch API requests I used a API Hub called RapidAPI which helps developers find and connect to tens of thousands of public APIs across multiple cloud environments.

As the user gets access to the Index page he will be able to choose his Language and topic preferences and click the Search button that will redirect him to a second page called News that will display in grid formatting all the latest news given as response (in JSON format) from the Bing API request related to user's search query string, ordered by publication date. This page will also advise the user by a Flash message to sign up and Login to have access to features like saving or sharing favorites articles.

The Register and Login pages use Flask forms and JavaScript functions to validate and store input from user such as username, email and password. As the criteria for each of them is met the user will be logged in by Flask-Login (which provides user session management) and redirected to his own personalized private page where he will be able to see and filter his favorites articles that can now be saved and shared from News page. The share button allows user to email the news URL along a default message that can be changed as desired.

In addition to session features, users are allowed to change password if logged in or reset password if forgotten. This is accomplished by Flask-mail, which sends an email to the user with a reset link attached to a 8 minute expiration token that redirects to a **reset_password** html page.

All the information collected by inputs on the flask forms and routes of the website such as registration and login details, news articles provided by the API and articles saved as favorites by users are stored in a database file named finalproject.db. Those informations are then accessed by SQLite3 commands to, for example, start a user session based in the user_id or display in the personal page all the user's favorite articles.

Sensitive information as API key, passwords and SECRET_KEY are stored in local file as environment variables in a file called ***.env*** and prevented to be pushed to an open repository by .gitignore.

The folder and files used and attached to this project are as follows:

. flask_session 
. static { images } { script.js } { styles.css } 
. templates { index.html } { layout.html } { login.html } { my_list.html } { my_filtered_list.html } { news.html } { register.html } { reset_password } { change_password } { forgot_password }
. app.py 
. helpers.py 
. finalproject.db 
. requirements.txt (packages on which this project depends)

This was a challenging but fun final task that allowed me to test all my new developing skills learnt at CS50. Hope you'll enjoy browsing!
