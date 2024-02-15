import re
from datetime import datetime
import os

from flask import Flask
from markupsafe import Markup, escape
from jinja2 import pass_eval_context

from . import posts, posts_admin, auth, common, users_admin


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(common.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(users_admin.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(posts_admin.bp)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    @app.template_filter("nl2br")
    @pass_eval_context
    def nl2br(eval_ctx, value):
        br = "<br>\n"

        if eval_ctx.autoescape:
            value = escape(value)
            br = Markup(br)

        result = "\n\n".join(
            f"<p>{br.join(p.splitlines())}</p>"
            for p in re.split(r"(?:\r\n|\r(?!\n)|\n){2,}", value)
        )
        return Markup(result) if eval_ctx.autoescape else result

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
