from flask import Flask, render_template
from blog.views.users import users_app
from blog.views.auth import auth_app, login_manager
from blog.views.articles import articles_app
from blog.models.database import db


app = Flask(__name__)
app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.models import User
    admin = User(username="administrator", is_staff=True)
    james = User(username="jameson")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)

