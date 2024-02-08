
from flask import render_template
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash


bp = Blueprint('users', __name__, url_prefix='/users')
dbname = get_database()
users = dbname["users"]


@bp.route("/")
def list():
    if 'user_id' not in session or session['user_id'] is None:
        return render_template('login.html')
    rows = users.find()
    auth = {}
    auth['authenticated'] = True
    auth['username'] = session['username']
    return render_template('users/list.html', users=rows, auth=auth)

@bp.route("/<id>")
def view(id):
    row = users.find_one({'_id':ObjectId(id)})
    return render_template('users/view.html', user=row)

@bp.route("/delete/<id>", methods=['POST'])
def delete(id):
    users.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('users.list'))

@bp.route("/new/", methods=['POST', 'GET'])
def new():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hash = generate_password_hash(password)
        doc = {
            "username": username,
            "password": hash
        }
        users.insert_one(doc)
        return redirect(url_for('users.list'))
    return render_template('users/new.html')

@bp.route("/edit/<id>", methods=['POST', 'GET'])
def edit(id):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        updated = {'$set': {'password': password, "username": username}}
        users.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for('users.list'))
    row = users.find_one({'_id':ObjectId(id)})
    return render_template('users/edit.html', user=row)