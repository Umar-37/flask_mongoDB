
from flask import Blueprint, redirect, render_template, url_for


bp = Blueprint("common", __name__, url_prefix="/")

@bp.route("/")
def home():
    return redirect(url_for("posts.list"))

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/links")
def link_list():
    return render_template("about.html")
