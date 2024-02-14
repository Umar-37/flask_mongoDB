from bson.objectid import ObjectId
from flask import Blueprint, render_template, request

from .auth import login_required
from .db import get_database

bp = Blueprint('posts', __name__, url_prefix='/posts')

dbname = get_database()
posts = dbname["posts"]


@bp.route("/")
def list():
    page_size = 10
    current_page = int(request.args.get('page', 1))
    skip = (current_page - 1) * page_size
    pipeline = [
        {'$sort': {'date': -1}},
        {'$skip': skip},
        {'$limit': page_size}
    ]
    rows = posts.aggregate(pipeline)
    total_posts = posts.count_documents({})
    pages = (total_posts + page_size - 1) // page_size
    return render_template('posts/list.html', posts=rows, pages=pages, current_page=current_page)

@bp.route("/<id>")
def view(id):
    row = posts.find_one({'_id':ObjectId(id)})
    return render_template('posts/view.html', post=row)
