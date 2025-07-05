from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

db=SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Text, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False) #
    password = db.Column(db.String(200), nullable=False) #

    login_count = db.Column(db.Integer) 
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))

    active = db.Column(db.Boolean) #
    fs_uniquifier = db.Column(db.String(255), unique=True) #
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) #
    description = db.Column(db.String(255))

class roles_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)