#! python
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators
import mysql_db_helper

app = Flask(__name__)
app.debug = True

# Config MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerQWER1234!@#$' # Change this to w/e your db password is
app.config['MYSQL_DB'] = 'issue_tracker_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM issues_tbl")

    issues = cur.fetchall()
    if not issues:
        issues = []
    cur.close()

    return render_template('index.html', issues=issues)

@app.route('/issues')
def issues():
    # Retrieve issues from DB and display them to the user
    cur = mysql.connection.cursor()

    # Grab all of the issues
    result = cur.execute("SELECT * FROM issues_tbl")
    issues = cur.fetchall()

    cur.close()

    return render_template('issues.html', issues=issues)

class IssueForm(Form):
    projectName = StringField('Project Name', [validators.Length(min=1, max=100)])
    title = StringField('Title', [validators.Length(min=10, max=200)])
    description = TextAreaField('Description', [validators.Length(min=1)])
    links = TextAreaField('Links')

@app.route('/add_issue', methods=["GET", "POST"])
def add_issue():
    form = IssueForm(request.form)
    if request.method == "POST" and form.validate():
        projectName = form.projectName.data
        title = form.title.data
        description = form.description.data
        links = form.links.data

        # Add the issue to the DB
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO issues_tbl(projectKey, title, description, links) VALUES(%s, %s, %s, %s)", (projectName, title, description, links))

        mysql.connection.commit()
        # Close the connection
        cur.close()
        flash("Issue added.", "success")
        return redirect(url_for("issues"))
        
    return render_template('add_issue.html', form=form)

@app.route('/delete_issue/<string:id>', methods=["POST"])
def delete_issue(id):
    # Remove the issue from the db
    cur = mysql.connection.cursor()
    result = cur.execute("DELETE FROM issues_tbl WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Issue deleted.", "success")
    return redirect(url_for('issues'))

@app.route('/view_issue/<string:id>')
def view_issue(id):
    # Retrieve the issue from the db and display its info to the user
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM issues_tbl WHERE id = %s", [id])
    issue = cur.fetchone()
    cur.close()

    return render_template('view_issue.html', issue = issue)

@app.route('/edit_issue/<string:id>', methods=['GET', 'POST'])
def edit_issue(id):
    # Retrieve issue from db and throw its info into a form like in the new_issue function
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM issues_tbl WHERE id = %s", [id])
    issue = cur.fetchone()
    cur.close()

    form = IssueForm(request.form)
    form.projectName.data = issue["projectKey"]
    form.title.data = issue["title"]
    form.description.data = issue["description"]
    form.links.data = issue["links"]

    if request.method == "POST" and form.validate():
        projectName = request.form["projectName"]
        title = request.form["title"]
        description = request.form["description"]
        links = request.form["links"]

     # Add the issue to the DB
        cur = mysql.connection.cursor()

        cur.execute("UPDATE issues_tbl SET projectKey = %s, title = %s, description = %s, links = %s WHERE id = %s", (projectName, title, description, links, id))

        mysql.connection.commit()
        # Close the connection
        cur.close()
        flash("Issue updated.", "success")
        return redirect(url_for('issues'))

    return render_template('edit_issue.html', issue=issue, form=form)


if __name__ == "__main__":
    mysql_db_helper.checkAndMakeDB()
    app.secret_key = "123abc" # Change this to something more secure
    app.run(port=5003)