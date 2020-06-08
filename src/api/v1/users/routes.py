import flask
from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth

from .. import application
from .. import db
from ..models import Users

auth = HTTPBasicAuth()


@application.route('/<path:text>', methods=['GET', 'POST'])
# handle all undefined endpoints
def re_route(text):
    return jsonify({'Message': 'Unrecognised endpoint'})


@auth.verify_password
def verify_password(email, password):
    email = email.lower()
    user = Users.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@application.route('/api/v1/users/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify({'Message': 'Input the user details in json format'})

    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    c_password = request.json.get('c_password')
    if password != c_password:
        return jsonify({'Message': 'Passwords do not match'})
    if name is None or password is None or email is None:
        return jsonify({'Message': 'One or more missing arguments'})
    if Users.query.filter_by(name=name).first() is not None:
        return jsonify({'Message': 'User already exists'})
    email = email.lower()
    user = Users(name=name, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': user.name})


@application.route('/api/v1/users/login', methods=['POST'])
@auth.login_required
def login():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
