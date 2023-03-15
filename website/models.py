from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Note is the name of the table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pts = db.Column(db.Integer)
    rbs = db.Column(db.Integer)
    asts = db.Column(db.Integer)
    stls = db.Column(db.Integer)
    tos = db.Column(db.Integer)
    blks = db.Column(db.Integer)
    mins = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class StatSnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statline = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    game_date = db.Column(db.String(100))
    team1 = db.Column(db.String(100))
    team2 = db.Column(db.String(100))
    video = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    stats = db.relationship('Stat')
    statsnapshots = db.relationship('StatSnapshot')
