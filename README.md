# JobHunt
## A simple job posting tracking site

JobHunt is a job posting tracking system created using Flask, Bootstrap (for now), and MySQL. JobHunt can be used to track job postings that a user is interested in across all sorts of different job listing websites (Indeed, LinkedIn, etc).

### Most engineers just use an Excel spreadsheet. Why not do that?

Great question. Originally, when I built FITS (an issue tracking Flask app), I was also tracking job postings I came across across the job posting sites on a Google Sheets spreadsheet, and it worked OK, but I felt that I could use the FITS infrastructure to build a nicer looking job tracker. My spreadsheet had a bunch of columns, and some of them had a lot of text in them, and it looked messy. It got to the point where some jobs had several lines of text (think 5-10 lines) in some columns, I was having to scroll, I was losing my place sometimes, it was messy to edit, etc.

To sum it up, I used to use a spreadsheet, it got messy, I already had the infrastructure for something cleaner, so I built something cleaner.

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
And your site will be live! With the default settings in app.py, you can access your site at localhost:5004. 