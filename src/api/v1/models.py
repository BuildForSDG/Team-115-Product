from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

from . import db
from . import application


class Users(db.Model):
    # user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))

    def __repr__(self):
        return '{}'.format(self.name)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(application.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(application.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = Users.query.get(data['id'])
        return user


class Solutions(db.Model):
    # solutions table
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    sector = db.Column(db.String(70), index=True)
    industry = db.Column(db.String(120), index=True, )
    industry_group = db.Column(db.String(120), index=True)
    sub_industry = db.Column(db.String(120), index=True)
    details = db.Column(db.Text, index=True)
    best_for = db.Column(db.String(120), index=True)
    contact_details = db.Column(db.String(120), index=True)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r}, {self.details!r}, {self.best_for!r}, {self.details!r})')
