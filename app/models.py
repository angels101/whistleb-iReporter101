from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, timezone, time, timedelta
from wtforms.fields.core import SelectField

@login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True, nullable=False)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash=db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    cases = db.relationship("Case", backref="user", lazy="dynamic")

    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
        raise AttributeError('You cannot access the password')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'User {self.username}'

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash=db.Column(db.String(255))
    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
        raise AttributeError('You cannot access the password')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'Admin {self.username}'

class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255)) # corruption or intervention
    title = db.Column(db.String(255))
    description = db.Column(db.String(255), index = True)
    image = db.Column(db.String(255))
    video = db.Column(db.String(255))
    geolocation = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"))

    def __repr__(self):
        return f"Case {self.title}"

    @classmethod
    def get_case(cls,id):
        cases = Case.query.filter_by(id=id).all()
        return cases

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"Role {self.name}"


class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))
    cases = db.relationship(
        "Case", backref="status", lazy="dynamic"
    )  # admin altering the status
    
    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return f"Status {self.status}