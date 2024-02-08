
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_bcrypt import Bcrypt


bp = Blueprint('users', __name__, url_prefix='/users')
dbname = get_database()
users = dbname["users"]
bcrypt = Bcrypt()


@bp.route("/")
def list():
    if 'user_id' not in session or session['user_id'] is None:
        return render_template('login.html')
    dbname = get_database()
    collection_name = dbname["users"]
    rows = collection_name.find()
    auth = {}
    auth['authenticated'] = True
    auth['username'] = session['username']
    return render_template('users/list.html', users=rows, auth=auth)

@bp.route("/<id>")
def view(id):
    rows = users.find({'_id':ObjectId(id)})
    return render_template('users/view.html', user=rows[0])

@bp.route("/delete/<id>", methods=['POST'])
def delete(id):
    users.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('users.list'))

@bp.route("/new/", methods=['POST', 'GET'])
def new():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
        doc = {
            "username": username,
            "password": hash
        }
        users.insert_one(doc)
        return redirect(url_for('users.list'))
    return render_template('users/new.html')

@bp.route("/edit/<id>", methods=['POST', 'GET'])
def edit(id):
    rows = users.find({'_id':ObjectId(id)})
    if request.method == "GET":
        return render_template('users/edit.html', user=rows[0])
    else:
        username = request.form["username"]
        password = request.form["password"]
        updated = {'$set': {'password': password, "username": username}}
        users.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for('users.list'))
