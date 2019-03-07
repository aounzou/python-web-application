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

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerData', methods=['GET', 'POST'])
def registerData():

    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    if email != "" and password != "":
        etat = "false"
        with sqlite3.connect('database.db') as con:
            try:
                if is_exist(email):
                    etat = json.dumps({'error': False}), 404, {'ContentType': 'application/json'}
                else:
                    cur = con.cursor()
                    cur.execute(
                        'INSERT INTO users (password, email, firstName, lastName) VALUES (?, ?, ?, ?)',
                        (hashlib.md5(password.encode()).hexdigest(), email, firstname, lastname))
                    con.commit()

                    msg = "Registered Successfully"
                    etat = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            except:
                con.rollback()
                msg = "Error occured"
                etat = json.dumps({'error': False}), 404, {'ContentType': 'application/json'}
        con.close()

    return etat




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



def is_exist(email):

    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email FROM users')
    data = cur.fetchall()

    for row in data:
        if row[0] == email:
            return True
    return False


def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            idUser = ''
        else:
            loggedIn = True
            cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
            userId = cur.fetchone()

    conn.close()
    return (loggedIn, userId)



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()