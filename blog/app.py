from flask import Flask
import commands
from extensions import db, login_manager, migrate, csrf
from models import User
from security import flask_bcrypt
from blog.views.authors import authors_app
from blog.admin import admin


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    flask_bcrypt.init_app(app)
    return app


def register_extensions(app):
    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from auth.views import auth
    from user.views import user

    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(authors_app, url_prefix="/authors")


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")
