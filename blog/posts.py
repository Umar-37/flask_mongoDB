from bson.objectid import ObjectId
from flask import Blueprint, render_template, request

from .auth import login_required
from blog.db import get_db
from .utils import pagination


bp = Blueprint("posts", __name__, url_prefix="/posts")

@bp.route("/")
def list():
    current_page = int(request.args.get("page", 1))
    ctx = pagination("posts", current_page)
    rows = ctx["rows"]
    return render_template("posts/list.html", posts=rows, ctx=ctx)

@bp.route("/<id>")
def view(id):
    posts_col = get_db("posts")
    row = posts_col.find_one({"_id":ObjectId(id)})
    return render_template("posts/view.html", post=row)
