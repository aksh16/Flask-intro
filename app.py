from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = "lkafjd;g1978"
app.database = ("sample.db")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You haven't logged in yet!")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
	g.db = db_connect()
	curs = g.db.execute("SELECT * FROM posts")
	posts = [dict(title = row[0], description = row[1]) for row in curs.fetchall()]
	g.db.close()
	return render_template("index.html", posts = posts)

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'aksh' or  request.form['password'] != 'patel':
			error = "Invalid username or password. Please try again"
		else:
			session['logged_in'] = True
			flash("You were just logged in!")
			return redirect(url_for('home'))
	return render_template('login.html', error = error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash("You were just logged out!")
	return redirect(url_for('welcome'))

def db_connect():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug = True)
