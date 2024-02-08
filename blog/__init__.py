from flask import Flask
from . import posts, posts_admin, auth, common, users_admin
from datetime import datetime


def create_app():
    # create and configure the app
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
    def nl2br(value):
        lines = value.split('\n')
        lines =[f"<p>{line}</p>" for line in lines if line.strip() != '']
        return '\n'.join(lines)


    return app
