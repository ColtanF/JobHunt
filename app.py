#! python
from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import mysql_db_helper
from functools import wraps

app = Flask(__name__)
app.debug = True

# Config MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerQWER1234!@#$' # Change this to w/e your db password is
app.config['MYSQL_DB'] = 'job_tracker_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)

# Check if user logged in
def isLoggedIn(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please log in to continue.', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    jobs = []
    if 'logged_in' in session:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM jobs_tbl WHERE username = %s", [session["username"]])

        jobs = list(cur.fetchall())
        jobs.sort(key=lambda x: x['rating'])

        if not jobs:
            jobs = []
        cur.close()
    return render_template('index.html', jobs=jobs)

@app.route('/jobs')
@isLoggedIn
def jobs():
    # Retrieve job postings from DB and display them to the user
    cur = mysql.connection.cursor()

    # Grab all of the jobs
    result = cur.execute("SELECT * FROM jobs_tbl WHERE username = %s", [session["username"]])
    jobs = cur.fetchall()

    cur.close()

    return render_template('jobs.html', jobs=jobs)


class JobForm(Form):
    company = StringField('Company Name', [validators.Length(min=1, max=100)])
    position = StringField('Position', [validators.Length(min=10, max=200)])
    companyInfo = TextAreaField('Company Description', [validators.Length(min=1)])
    positionInfo = TextAreaField('Position Description', [validators.Length(min=1)])
    reqsIMeet = TextAreaField('Requirements I meet')
    reqsIDontMeet = TextAreaField('Requirements I don\'t meet')
    address = StringField('Address', [validators.Length(min=1, max=300)])
    links = TextAreaField('Links')
    salary = StringField('Salary', [validators.Length(max=200)])
    status = StringField('Status', [validators.Length(min=1, max=200)])

@app.route('/add_job', methods=["GET", "POST"])
@isLoggedIn
def add_job():
    form = JobForm(request.form)
    if request.method == "POST" and form.validate():
        company = form.company.data
        position = form.position.data
        companyInfo = form.companyInfo.data
        positionInfo = form.positionInfo.data
        address = form.address.data
        links = form.links.data
        status = form.status.data
        reqsIMeet = form.reqsIMeet.data
        reqsIDontMeet = form.reqsIDontMeet.data
        salary = form.salary.data

        # Add the job to the DB
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO jobs_tbl(company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, username, rating) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)", 
                    (company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, session["username"]))

        mysql.connection.commit()
        # Close the connection
        cur.close()
        flash("Job added.", "success")
        return redirect(url_for("jobs"))
        
    return render_template('add_job.html', form=form)

@app.route('/delete_job/<string:id>', methods=["POST"])
@isLoggedIn
def delete_job(id):
    # Remove the job from the db
    cur = mysql.connection.cursor()
    result = cur.execute("DELETE FROM jobs_tbl WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Job deleted.", "success")
    return redirect(url_for('jobs'))

@app.route('/view_job/<string:id>', methods=['GET', 'POST'])
@isLoggedIn
def view_job(id):
    # Retrieve the job from the db and display its info to the user
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM jobs_tbl WHERE id = %s", [id])
    job = cur.fetchone()
    cur.close()
    if request.method == "POST": 
        # rating must have been updated. Update the rating in the db
        ratingsForm = request.form
        if ratingsForm['stars']:
            cur = mysql.connection.cursor()
            result = cur.execute("UPDATE jobs_tbl SET rating = %s WHERE id = %s", [ratingsForm['stars'], id])
            mysql.connection.commit()
            result = cur.execute("SELECT * FROM jobs_tbl WHERE id = %s", [id])
            job = cur.fetchone()
            cur.close()
            flash("Rating updated.", "success")

        return render_template('view_job.html', job=job)


    return render_template('view_job.html', job = job)

@app.route('/edit_job/<string:id>', methods=['GET', 'POST'])
@isLoggedIn
def edit_job(id):
    # Retrieve job from db and throw its info into a form like in the add_job function
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM jobs_tbl WHERE id = %s", [id])
    job = cur.fetchone()
    cur.close()

    form = JobForm(request.form)
    form.company.data = job["company"]
    form.position.data = job["position"]
    form.positionInfo.data = job["positionInfo"]
    form.reqsIMeet.data = job["reqsIMeet"]
    form.reqsIDontMeet.data = job["reqsIDontMeet"]
    form.salary.data = job["salary"]
    form.address.data = job["address"]
    form.status.data = job["status"]
    form.companyInfo.data = job["companyInfo"]
    form.links.data = job["links"]

    if request.method == "POST" and form.validate():
        company = request.form["company"]
        position = request.form["position"]
        positionInfo = request.form["positionInfo"]
        companyInfo = request.form["companyInfo"]
        reqsIMeet = request.form["reqsIMeet"]
        reqsIDontMeet = request.form["reqsIDontMeet"]
        salary = request.form["salary"]
        address = request.form["address"]
        status = request.form["status"]
        links = request.form["links"]


     # Add the job to the DB
        cur = mysql.connection.cursor()

        cur.execute("UPDATE jobs_tbl SET company = %s, position = %s, companyInfo = %s, positionInfo = %s, reqsIMeet = %s, reqsIDontMeet = %s, salary = %s, address = %s, links = %s, status = %s WHERE id = %s", 
                    (company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, id))
        mysql.connection.commit()
        
        # Grab the updated job
        result = cur.execute("SELECT * FROM jobs_tbl WHERE id = %s", [id])
        job = cur.fetchone()

        # Close the connection
        cur.close()
        flash("Job updated.", "success")
        return redirect(url_for("view_job", id=id))

    return render_template('edit_job.html', job=job, form=form)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Need to add user to database
        # Create cursor
        cur = mysql.connection.cursor()
        # First, check if the username is already taken
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        mysql.connection.commit()
        data = cur.fetchall()
        if len(data) != 0:
            flash("Account with username " + username + " already exists, please choose a different username.", "warning")
            return render_template('register.html', form=form)

        # If the username is unique, add it to the database
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to db
        mysql.connection.commit()

        cur.close()
        flash("You are now registered and can login.", 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # get the fields from the page
        username = request.form["username"]
        password_candidate = request.form["password"]

        # DB Stuff
        # Create cursor
        cur = mysql.connection.cursor()

        # Check for username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            cur.close()

            # Compare the passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info("PASSWORD MATCHED!")
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in.', 'success')
                return redirect(url_for('index'))
            else:
                print("I am here")
                error = "Invalid password."
                app.logger.info(error)
                return render_template('login.html', error=error)
        else: 
            # invalid username
            error = "Invalid username."
            app.logger.info(error)
            return render_template('login.html', error=error)

    return render_template("login.html")

@app.route('/logout')
@isLoggedIn
def logout():
    session.clear()
    flash("You are now logged out.", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    mysql_db_helper.checkAndMakeDB()
    app.secret_key = "123abc" # Change this to something more secure
    app.run(port=5004)