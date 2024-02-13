
import sys
import click

from getpass import getpass
from flask import render_template, flash
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from .auth import login_required


bp = Blueprint('users_admin', __name__, url_prefix='/admin/users')
dbname = get_database()
users = dbname["users"]

@bp.cli.command('create')
@click.argument('username')
def create(username):
    user = users.find_one({'username': username})
    if user is not None:
        print("User already exists")
        sys.exit(1)
    password = getpass()
    data = {
            "username": username,
            "password": generate_password_hash(password),
    }
    users.insert_one(data)
    print(f"user \"{username}\" created")


@bp.cli.command('reset')
@click.argument('username')
def reset(username):
    user = users.find_one({'username': username})
    if user is None:
        print("User does not exist")
        sys.exit(1)
    password = getpass()
    query = {'username': username}
    data = {
        "$set": {
            "username":username,
            "password": generate_password_hash(password),
        }
    }
    users.update_one(query, data)
    print(f"user \"{username}\" password changed")

@bp.route("/")
@login_required
def list():
    rows = users.find()
    return render_template('admin/users/list.html', users=rows)

@bp.route("/delete/<id>", methods=['POST'])
@login_required
def delete(id):
    users.delete_one({'_id':ObjectId(id)})
    flash("User deleted")
    return redirect(url_for('users_admin.list'))

@bp.route("/new/", methods=['POST', 'GET'])
@login_required
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
        return redirect(url_for('users_admin.list'))
    return render_template('admin/users/new.html')

@bp.route("/edit/<id>", methods=['POST', 'GET'])
@login_required
def edit(id):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash = generate_password_hash(password)
        updated = {'$set': {'password': hash, "username": username}}
        users.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for('users_admin.list'))
    row = users.find_one({'_id':ObjectId(id)})
    return render_template('admin/users/edit.html', user=row)
