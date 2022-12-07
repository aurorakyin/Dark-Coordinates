# Dark Coordinates

## CS50
>This is our final project for the CS50 Introduction to Computer Sciense course!
Documentation for your project in the form of a Markdown file called README.md. This documentation is to be a user’s manual for your project. Though the structure of your documentation is entirely up to you, it should be incredibly clear to the staff how and where, if applicable, to compile, configure, and use your project. Your documentation should be at least several paragraphs in length. It should not be necessary for us to contact you with questions regarding your project after its submission. Hold our hand with this documentation; be sure to answer in your documentation any questions that you think we might have while testing your work.

## What is it?
Our final project is a website that guides you through a small tour of the supernatural world. With the navigation bar, you will be able to access different parts of our website, such as one that hosts information about a variety of ghosts and one that teaches about 

We also use a database (darkcoor.db) that allows the viewer to register as a user and save their favorite supernatural stories.
sqlite3 is used to manage the database. This database is tracking both the user's username and password, as well as the favorited ghost stories of the user if they have registered an account. We compiled and configured this project using the CS50 VS codespace, which is where our website currently lives (using flask run). Once all the files have been downloaded and flask run has been run, the website should begin with a navigation bar with the options to register an account or login, and the homepage should be a snippet of a google map with four markers that also serve as hyperlinks. Each marker corresponds to a ghost story from the place that the marker is placed on the world map. If the user decides not to register an account, then the website serves its purpose as a place to find and read ghost stories. 

However, if the user decides to register an account, then he/she should press the "register" button in the top right. From there, you will be redirected to a webpage asking the user to create a username and password, which after submitting, should redirect you to the homepage with the google map snippet in the newly-made account. There, the navigation bar will have new options: Directory, how to, Mental Haven, and Me. 

Pressing Directory will redirect the user to a webpage including a snippet of a wikipedia page of a list of urban legends, as well as the four ghost stories that we have included on the website. 

Hovering over how to will lead to two options: get in contact with Ghost, and avoid contact with Ghost. Pressing on get in contact with ghost will lead to a webpage with some tips and tricks as to how to get in contact with ghosts, as well some links for more information. We also included a snippet of an article on how to become a psychic. Pressing on avoid contact with ghost will lead to a webpage with the same structure as the other webpage, except the tips and tricks are how to avoid contact.

Next, is Mental Haven. Clicking on this will redirect the user to a webpage with many youtube videos meant to help the user decompress and stop being scared after reading the ghost stories. We have included cute videos of dogs and at the bottom there is a button the user can press as much as he/she wants to decompress as well.



### darkcoord.db
This database includes two tables, one with information about the users and the other.

## Parts of the website
- Register and Login page (where you become one of the boos!)

| Login | Register |
| :---: | :---: |
| <img src="" width="400">  | <img src="" width="400">|

- Homepage and directory

| Homepage | Directory |
| :---: | :---: | 
| <img src="" width="400"> | <img src="" width = "400">

- Avoid Contact and Get in Contact

| Homepage | Directory |
| :---: | :---: | 
| <img src="" width="400"> | <img src="" width = "400">

## Video Walkthrough
You can also watch us talk about the project on Youtube at this link:
[Final Project: Dark Coordinates](link to be inserted)
