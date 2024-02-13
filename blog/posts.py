from bson.objectid import ObjectId
from flask import Blueprint, render_template

from .auth import login_required
from .db import get_database

bp = Blueprint('posts', __name__, url_prefix='/posts')

dbname = get_database()
posts = dbname["posts"]


@bp.route("/")
def list():
    rows = posts.find().sort({'date':-1})
    return render_template('posts/list.html', posts=rows)

@bp.route("/<id>")
def view(id):
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('posts/view.html', post=row)
