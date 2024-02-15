import datetime

from faker import Faker
from flask import  Blueprint, redirect, render_template, request, url_for
from bson.objectid import ObjectId
import click

from .auth import login_required
from blog.db import get_db


fake = Faker()
bp = Blueprint("posts_admin", __name__, url_prefix="/admin/posts")

@bp.cli.command("seed_test_data")
@click.argument("number", type=int)
def seed_test_data(number):
    posts_col = get_db("posts")
    # Seed posts
    for i in range(number):
        doc = {
            "title": fake.sentence(3),
            "body": "\n\n".join(fake.paragraphs()),
            "date": datetime.datetime.now()
        }
        posts_col.insert_one(doc)

    print("Done seeding")

@bp.route("/")
def list():
    posts_col = get_db("posts")
    rows = posts_col.find({}, {"title":1})
    return render_template("admin/posts/list.html", posts=rows)

@bp.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):
    posts_col = get_db("posts")
    posts_col.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("posts_admin.list"))

@bp.route("/new/", methods=["POST", "GET"])
@login_required
def new():
    posts_col = get_db("posts")
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        doc = {
            "title": title,
            "date": datetime.datetime.now(),
            "body": body
        }
        posts_col.insert_one(doc)
        return redirect(url_for("posts_admin.list"))
    return render_template("admin/posts/new.html")

@bp.route("/edit/<id>", methods=["POST", "GET"])
@login_required
def edit(id):
    posts_col = get_db("posts")
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        updated = {
            "$set": {
            "body": body, "title": title
            },
            "$currentDate": {
                "date": {"$type": "date"}
            }}
        posts_col.update_one({"_id":ObjectId(id)}, updated)
        return redirect(url_for("posts_admin.list"))
    row = posts_col.find_one({"_id":ObjectId(id)})
    return render_template("admin/posts/edit.html", post=row)
