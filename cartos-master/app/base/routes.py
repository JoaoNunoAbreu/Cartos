#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import login_manager, create_app, token_required,neo4j_db
from app.base import blueprint
import re

###### este é meu
from flasgger import swag_from
from flask import jsonify
from bson import json_util
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import jwt
CORS(blueprint)


@blueprint.route('/login', methods=['POST'])
@swag_from('docs/login-post.yml')
def login():

    _id = request.form.get('id')
    print(f"_id: {_id}")
    password = request.form.get('password')
    user = neo4j_db.evaluate(f'match (x:User) where x._id="{_id}" return x')
    print(f"user: {user}")

    if user and check_password_hash(user["password"], password):
        users= neo4j_db.evaluate('match (x:User) return x')
        nome = request.args.get('nome')

        token = jwt.encode({
            'sub': _id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=720)},
            '\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i' #jwt app.config['SECRET_KEY']
        )
        return json_util.dumps({'token': token.decode('UTF-8'), 'user':user, 'users': users, 'nome': nome})
    elif(user == None):
        return json_util.dumps({'error': 'O utilizador não existe!'},indent=4,ensure_ascii=False)
    else:
        return json_util.dumps({'error': 'Password incorrecta!'},indent=4,ensure_ascii=False)



@blueprint.route('/logout')
@token_required
#@login_required
@swag_from('docs/logout.yml')
def logout():

    print("logging out")
    return json_util.dumps({'message': 'Logged out!'})
