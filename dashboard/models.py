from dashboard import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from dateutil import tz

db = SQLAlchemy(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    github_login = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    comment = db.Column(db.String(256))

    solves = db.relationship("Solve")

    def __init__(self, github_id, github_login, nickname, comment):
        self.id = github_id
        self.github_login = github_login
        self.nickname = nickname
        self.comment = comment

    def __repr__(self):
        return f"<User {self.id} github_login={self.github_login} nickname={self.nickname}>"

class Lab(db.Model, SerializerMixin):
    __tablename__ = 'lab'
    repo_name = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    category = db.Column(db.String(256))
    author = db.Column(db.String(256))
    url = db.Column(db.String(256))
    flag = db.Column(db.String(256))
    detail = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now())

    solvers = db.relationship("Solve")

    def __init__(self, repo_name, name, category, author, url, flag, detail):
        self.repo_name = repo_name
        self.name = name
        self.author = author
        self.category = category
        self.url = url
        self.flag = flag
        self.detail = detail

    def __repr__(self):
        return f"<Lab {self.id} name={self.name} category={self.category} author={self.author}>"

class Solve(db.Model):
    __tablename__ = 'solve'

    serialize_rules = ('solved_at')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    lab_repo_name = db.Column(db.String(100), db.ForeignKey('lab.repo_name'), primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User")
    lab = db.relationship("Lab")

    def __init__(self, user_id, lab_repo_name):
        self.user_id = user_id
        self.lab_repo_name = lab_repo_name

    def solved_at(self):
        utc = self.create_at
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(app.config['TIMEZONE'])

        utc = utc.replace(tzinfo=from_zone)

        return utc.astimezone(to_zone)

    def __repr__(self):
        return f"<Solve user_id={self.user_id} lab_repo_name={self.lab_repo_name}>"

db.create_all()