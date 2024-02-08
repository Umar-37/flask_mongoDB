from flask import Flask, redirect, url_for, render_template, request
from . import posts, users
from .db import get_database
from flask import (
     flash, g, redirect, render_template, request, session, url_for
)
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from . import users


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "secret"
    app.register_blueprint(posts.bp)
    app.register_blueprint(users.bp)
    dbname = get_database()
    users_col = dbname["users"]
    bcrypt = Bcrypt(app)

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        dbname = get_database()
        users = dbname['users']
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            rows = users_col.find({'username':username})
            # check = bcrypt.check_password_hash(rows[0]['password'],password)
            # print('-/-//-', check)
            error = None
            user = users.find_one({'username':username})
            if user is None:
                error = 'Incorrect username.'
            # elif not check_password_hash(user['password'], password):
                # error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                return redirect(url_for('home'))

            flash(error)
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.template_filter('nl2br')
    def nl2br(value):
        lines = value.split('\n')
        lines =[f"<p>{line}</p>" for line in lines if line.strip() != '']
        return '\n'.join(lines)

    @app.route("/")
    def home():
        return redirect(url_for('posts.list'))

    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/links")
    def link_list():
        return render_template('about.html')

    return app
