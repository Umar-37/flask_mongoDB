
from flask import Flask, render_template
from .db import get_database
from flask import request, redirect, url_for
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

bp = Blueprint('common', __name__, url_prefix='/')

dbname = get_database()
users = dbname["users"]


@bp.route("/")
def home():
    return redirect(url_for('posts.list'))

@bp.route("/about")
def about():
    return render_template('about.html')

@bp.route("/links")
def link_list():
    return render_template('about.html')
