from flask import *
from flask import render_template
import sqlite3, hashlib
import os
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def login2():
    return render_template('login.html')


@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    email = request.form['email']
    password = request.form['password']
    if email !="" and password!="":

        if is_valid(email, password):
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'error': False}), 404, {'ContentType': 'application/json'}



def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT userId,email, password FROM users')
    data = cur.fetchall()

    for row in data:
        if row[1] == email and row[2] == hashlib.md5(password.encode()).hexdigest():
            session['userId'] = row[0]
            return True
    return False

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()