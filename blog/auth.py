
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

dbname = get_database()
users = dbname["users"]


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username':username})
        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            return redirect(url_for('common.home'))

        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('common.home'))
