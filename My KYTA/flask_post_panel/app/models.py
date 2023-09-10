# ... models.py ...

from datetime import datetime
import pytz

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Float, default=0.0)  # текущий баланс пользователя

    panels = db.relationship('Panel', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_url = db.Column(db.String(36), unique=True, nullable=False)
    activated_on = db.Column(db.DateTime, index=True, default=None, nullable=True)  # Дата активации
    expires_on = db.Column(db.DateTime, index=True, default=None, nullable=True)    # Дата истечения
    last_accessed = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_requests = db.relationship('PostRequest', backref='panel', lazy=True)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'))

class PostRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panel_id = db.Column(db.String(36), db.ForeignKey('panel.id'), nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)