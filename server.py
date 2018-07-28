from flask import Flask, render_template, request, session, flash, redirect
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = 'definetlysekret'
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

mysql = MySQLConnector(app, 'emaildb')

@app.route('/', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        return render_template('results.html')
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def results():
    errors = False
    if request.method == 'POST':        
        if len(request.form['email']) < 1:
            flash("E-mail cannot be empty!")
            errors = True
        if not email_regex.match(request.form['email']):
            flash("Invalid Email Address!")
            errors = True
        if errors == True:
            return redirect('/')
        else:
            query = 'INSERT INTO users(email, created_at, updated_at) VALUES (:email, NOW(), NOW())'
            data = {
                "email": request.form['email']
            }
            mysql.query_db(query,data)
    return render_template('success.html')

        
        
app.run(debug = True)   