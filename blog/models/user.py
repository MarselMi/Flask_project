from blog.models.database import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    email = Column(String(255), nullable=False, default="", server_default="")

    _password = Column(LargeBinary, nullable=True)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)
