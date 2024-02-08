from flask import Flask
from . import users, posts, auth, common


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "secret"
    app.register_blueprint(common.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(posts.bp)

    @app.template_filter('nl2br')
    def nl2br(value):
        lines = value.split('\n')
        lines =[f"<p>{line}</p>" for line in lines if line.strip() != '']
        return '\n'.join(lines)


    return app
