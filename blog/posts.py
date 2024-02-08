
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('posts', __name__, url_prefix='/posts')

dbname = get_database()
posts = dbname["posts"]


@bp.route("/")
def list():
    rows = posts.find()
    auth = {}
    if session.get('user_id', None):
        auth['authenticated'] = True
        auth['username'] = session['username']
    else:
        auth['authenticated'] = False
    return render_template('posts/list.html', posts=rows, auth=auth)

@bp.route("/<id>")
def view(id):
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('posts/view.html', post=row)

@bp.route("/delete/<id>", methods=['POST'])
def delete(id):
    posts.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('posts.list'))

@bp.route("/new/", methods=['POST', 'GET'])
def new():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        doc = {
            "title": title,
            "body": body
        }
        posts.insert_one(doc)
        return redirect(url_for('posts.list'))
    return render_template('posts/new.html')

@bp.route("/edit/<id>", methods=['POST', 'GET'])
def edit(id):
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        updated = {'$set': {'body': body, "title": title}}
        posts.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for('posts.list'))
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('posts/edit.html', post=row)
