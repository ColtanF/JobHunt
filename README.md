# FITS
## The (Coltan) Franke Issue Tracking System

FITS is a software development project issue tracking system created using Flask, Bootstrap (for now), and MySQL. Fits is an issue tracking web site similar to other like JIRA, VersionOne, etc. 

### Why does this exist when other apps like JIRA and VersionOne exist? Even GitHub lets you track issues on projects.

Great question. Essentially, I have a bunch of side projects, and I wanted to be able to locally track issues/planned improvements across all of my side projects.

I wanted to build something from scratch, on my own, and I wanted to practice developing with Flask and MySQL. Beyond that, I wanted a tool specifically for me to host locally on my machine while I developed projects. I wanted something simple, with no licenses or extensive installation processes, a tool without a ton of features that I didn't need. I also wanted the ability to view all of the issues across all of my side projects, all in one place.

Essentially, I just wanted an issue tracking app that was a bit more extensive than a todo list app, so I built one. 

### If I also wanted an app like this, what would I need to do?

Well, if you'd like, you could start by checking out the code from this repo. Besides that, you'll need MySQL, Python (I used v3, but you could probably use V2 if you wanted, with a bit of retooling), pip, and several Python packages. The full list of Python packages is available in requirements.txt at the root of the project. You can use the following command within a Python virtual environment (or just on your computer if you want all of the Python packages for your global Python installation) to install all of the Python packages you need: 

```
pip install -r requirements.txt
```

Once you have all of that, you'll need to set up your MySQL installation (if you haven't already) and add a database with the name given in the app.py file with a table called issues_tbl. You can do this manually if you'd like, but this is now all taken care of by the mysql_db_helper.py file's only function, which creates the database and requisite table automatically. This file's function is called on Flask app startup, but you can comment it out and just run the mysql_db_helper function code on its own as well.

You will want to update the MySQL db config info in both the app.py and mysql_db_helper.py files to match your MySQL installation's config.

Once that's finished, run the following from the command line:
```
python app.py
```
And your site will be live! With the default settings in app.py, you can access your site at localhost:5003. 