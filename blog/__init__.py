from flask import Flask
from . import posts, posts_admin, auth, common, users_admin
from datetime import datetime
from markupsafe import Markup, escape
import re
from jinja2 import pass_eval_context




def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"
    app.register_blueprint(common.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(users_admin.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(posts_admin.bp)

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.template_filter('nl2br')
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

    return app
