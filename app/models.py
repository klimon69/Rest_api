from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(64), index=True, unique=True)
    reg_balance = db.Column(db.Integer)
    currency = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    send_from = db.Column(db.String(140))
    send_to = db.Column(db.String(140))
    send_amount = db.Column(db.Integer)

    def __repr__(self):
        return '<Transaction {}>'.format(self.send_from)