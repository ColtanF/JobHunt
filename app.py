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
app.config['MYSQL_DB'] = 'job_tracker_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM jobs_tbl")

    jobs = list(cur.fetchall())
    jobs.sort(key=lambda x: x['rating'])

    if not jobs:
        jobs = []
    cur.close()

    return render_template('index.html', jobs=jobs)

@app.route('/jobs')
def jobs():
    # Retrieve job postings from DB and display them to the user
    cur = mysql.connection.cursor()

    # Grab all of the jobs
    result = cur.execute("SELECT * FROM jobs_tbl")
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
        rating = 0

        # Add the job to the DB
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO jobs_tbl(company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, rating) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)", 
                    (company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status))

        mysql.connection.commit()
        # Close the connection
        cur.close()
        flash("Job added.", "success")
        return redirect(url_for("jobs"))
        
    return render_template('add_job.html', form=form)

@app.route('/delete_job/<string:id>', methods=["POST"])
def delete_job(id):
    # Remove the job from the db
    cur = mysql.connection.cursor()
    result = cur.execute("DELETE FROM jobs_tbl WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Job deleted.", "success")
    return redirect(url_for('jobs'))

@app.route('/view_job/<string:id>', methods=['GET', 'POST'])
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
        return render_template('view_job.html', job=job)

    return render_template('edit_job.html', job=job, form=form)


if __name__ == "__main__":
    mysql_db_helper.checkAndMakeDB()
    app.secret_key = "123abc" # Change this to something more secure
    app.run(port=5004)