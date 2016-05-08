#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import MySQLdb as mysql
from MySQLdb.cursors import DictCursor
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort,\
     render_template, flash


""" Configuration """
DEBUG = True
#SECRET_KEY = 'development key'
SECRET_KEY = os.urandom(24)
USERNAME = 'admin'
PASSWORD = 'admin'

""" Create my app """
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent= True)

def connect_db():
    """ Connects to the specific database """
    conn = mysql.connect( host="localhost", user="root", passwd="", db="flaskr")
    return  conn

@app.before_request
def before_request():
    """Make sure we are connected to the database each request"""
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def show_entries():
    cur = g.db.cursor(DictCursor)
    query = 'select title,text from entries order by id desc'
    cur.execute(query)
    entries = [dict(title = row['title'].decode('utf-8'), text = row['text'].decode('utf-8')) for row in cur.fetchall()]
    return render_template('show_entries.html', entries = entries)

@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    cur.execute('insert into entries (title, text) values(%s,%s)',
                [request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
    cur.close()
    g.db.commit()

    flash('New entry was sussessfully posted!')
    return redirect(url_for('show_entries'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password!'
        else:
            session['logged_in'] = True
            flash('You were logged_in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
