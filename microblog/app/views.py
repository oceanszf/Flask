#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import render_template
from app import app


@app.route('/')

@app.route('/index')
def index():
    user = {'nickname': 'jeffrey'}
    posts = [{
            'author': {'nickname': 'Jhon'},
            'body': 'Beatiful day in Portland!'
            },{
            'author': {'nickname': 'Susan'},
            'body': 'The avengers movie was so cool!'
            }
            ]
    return render_template("index.html", title="Home", user=user,posts=posts)
