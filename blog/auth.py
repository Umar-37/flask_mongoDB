import functools

from bson.objectid import ObjectId
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.before_app_request
def load_logged_in_user():
    users_col = get_db("users")
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = users_col.find_one({"_id":ObjectId(user_id)})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.route("/login", methods=("GET", "POST"))
def login():
    users_col = get_db("users")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users_col.find_one({"username":username})
        error = None
        if user is None or not check_password_hash(user["password"], password):
            error = "Incorrect credentials."

        if error is None:
            session.clear()
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            return redirect(url_for("common.home"))

        flash(error)
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("common.home"))
