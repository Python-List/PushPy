import datetime
from app import db

class adminUser(db.Model):
    __tablename__='adminuser'
    id=db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return '<User %s>' % self.email


class User(db.Model):
    __tablename__='user'
    userid=db.Column(db.Integer,primary_key=True)
    udid=db.Column(db.String(70),unique=True)
    language=db.Column(db.String(70),unique=True)
    push=db.Column(db.Boolean, default=0)
    last=db.Column(db.DateTime, default=datetime.date.today())
    token=db.Column(db.String(100))
    def __init__(self, udid=None,language=None,push=None,last=None,token=None):
        self.udid=udid
        self.language=language
        self.push=push
        self.token=token
        self.last=datetime.date.today()
    def __repr__(self):
        return '<User %s>' % self.username