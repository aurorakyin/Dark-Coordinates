# Designing Dark Coordinates

## Overview
we used Python, HTML, CSS, and JavaScript. We implemented this project by referencing past HW's that we did, such as finance and homepage.  

## app.py
Our app.py is based off of the app.py from the finance HW, and we maintained similar methods for the login and register portions of the app.py. We also added routes for all of our HTML pages, such as Directory, How to Avoid Contact with Ghosts, How to Contact Ghosts, Me, and each of our four ghost stories. 

## Login/Register
On Dark Coordinates, the view should be able to register for an account and interact with the website with their account, such as adding selected stories to their favorites. In order to store the information about the user and information about the favorited stories, we created a database.

## darkcoor.db
The Database is divided into two different tables. One of the tables stores information about the user, such as their chosen username and password hash. The other table in the database stores information about the stories that they want to save. We made the decision to use two separate tables for this, since the user information should be unique while each user should be able to save mulptiple stories.

## Index and other pages
We use a navigation bar that stays at the top of the webpage at all times so that the user can easily navigate through the website. Since most of our html files have the same structure, we used the block feature of jinja to shorten the code. We also made sure that the webpages are interconnected so that they form a net of information instead of standing alone. Features that we chose to include in the webpages include videos, imbedded websites, etc.

## Directory
The directory links to several stories that we chose to include in the website. It serves as a subhost of information that's slightly diffrent from other websites.
