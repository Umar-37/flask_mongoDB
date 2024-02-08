
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from bson.objectid import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .auth import login_required
bp = Blueprint('posts', __name__, url_prefix='/posts')

dbname = get_database()
posts = dbname["posts"]


@bp.route("/")
def list():
    rows = posts.find()
    return render_template('posts/list.html', posts=rows)

@bp.route("/<id>")
def view(id):
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('posts/view.html', post=row)
