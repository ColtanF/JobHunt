# FITS
## The (Coltan) Franke Issue Tracking System

FITS is a software development project issue tracking system created using Flask, Bootstrap (for now), and MySQL. Fits is an issue tracking web site similar to other like JIRA, VersionOne, etc. 

### Why does this exist when other apps like JIRA and VersionOne exist? Even GitHub lets you track issues on projects.

Great question. Essentially, I have a bunch of side projects, and I wanted to be able to locally track issues/planned improvements across all of my side projects.

I wanted to build something from scratch, on my own, and I wanted to practice developing with Flask and MySQL. Beyond that, I wanted a tool specifically for me to host locally on my machine while I developed projects. I wanted something simple, with no licenses or extensive installation processes, a tool without a ton of features that I didn't need. I also wanted the ability to view all of the issues across all of my side projects, all in one place.

Essentially, I just wanted an issue tracking app that was a bit more extensive than a todo list app, so I built one. 

### If I also wanted an app like this, what would I need to do?

Well, if you'd like, you could start by checking out the code from this repo. Besides that, you'll need MySQL, Python (I used v3, but you could probably use V2 if you wanted, with a bit of retooling), pip, and the following Python packages: flask, flask_mysqldb, and wtforms. (Note to self, should probably make a requirements.txt file for pip users). 

Once you have all of that, you'll need to set up your MySQL installation (if you haven't already) and add a database with the name given in the app.py file with a table called issues_tbl (this is also in app.py, but not as easy to spot as the DB name). You can structure the table however you want, but it needs to at least have the fields in it that match what is used in the SQL commands in app.py and referenced in the html templates. (Another note to self, I should add either a list of SQL commands I used in setting up the DB or a script that does that for the user when setting up the website).

Once your table is created, you will also want to replace the MySQL account/installation info at the top of the app.py file to be able to access the DB from the Flask app.

Once that's finished, all you should have to do is run 'python app.py' from the command line in the directory where the code is checked out.