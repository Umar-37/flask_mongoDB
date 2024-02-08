
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .auth import login_required
bp = Blueprint('posts_admin', __name__, url_prefix='/admin/posts')

dbname = get_database()
posts = dbname["posts"]


@bp.route("/")
def list():
    rows = posts.find()
    return render_template('admin/posts/list.html', posts=rows)

@bp.route("/delete/<id>", methods=['POST'])
@login_required
def delete(id):
    posts.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('posts_admin.list'))

@bp.route("/new/", methods=['POST', 'GET'])
@login_required
def new():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        doc = {
            "title": title,
            "body": body
        }
        posts.insert_one(doc)
        return redirect(url_for('posts_admin.list'))
    return render_template('admin/posts/new.html')

@bp.route("/edit/<id>", methods=['POST', 'GET'])
@login_required
def edit(id):
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        updated = {'$set': {'body': body, "title": title}}
        posts.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for('posts_admin.list'))
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('admin/posts/edit.html', post=row)
