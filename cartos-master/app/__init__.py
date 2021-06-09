#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, jsonify, Blueprint
from flask_login import LoginManager
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from bson.objectid import ObjectId
import json

###Imports
import datetime
from functools import wraps
import jwt
#########

login_manager = LoginManager()
dadosElemento = {}
indexList = []
tags = []
historic = [ ]


#################
@login_manager.user_loader
def user_loader(email):
    return None

from flasgger import Swagger

import os
from dotenv import load_dotenv
from py2neo import Graph
load_dotenv()
neo4j_db = Graph(os.getenv("DB_URL"),password=os.getenv("DB_PASS"), user=os.getenv("DB_USER"))
#################

def register_extensions(app):
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('home','users','elementos','analise','importacao','base'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def apply_themes(app):
    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith('static'):
            themename = values.get('theme', None) or \
                app.config.get('DEFAULT_THEME', None)
            if themename:
                theme_file = "{}/{}".format(themename, values.get('filename', ''))
                if path.isfile(path.join(app.static_folder, theme_file)):
                    values['filename'] = theme_file
        return url_for(endpoint, **values)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    apply_themes(app)

    swag = Swagger(app)
    return app


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            print("wrong len")
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            #print("BREAK 1")
            data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
            #print("BREAK 2")
            query = f'match (n:User) where n._id = "{data["sub"]}" return n'
            #print("BREAK 3")
            user = neo4j_db.evaluate(query)
            #print("BREAK 4")
            now = datetime.datetime.now()
            #print("BREAK 5")
            date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            #print("BREAK 6")
            did = ObjectId()
            #print("BREAK 7")
            reqstring= request.method + ":" + request.url
            #print("BREAK 8")
            if not user:
                raise RuntimeError('User not found')
           
            neo4j_db.evaluate('match (x {_id:$v}) set  x+={ativo:"true" , stamp:$date} return x',v=data['sub'],date=date)
            #print("BREAK 9")
            h = {"_id": str(did), "user":data['sub'], "stamp":date, "request":reqstring}
            #print("BREAK 10")

            with open('historic.json') as json_file:
                reqs = json.load(json_file)

            reqs.append(h)
            #print("BREAK 11")

            with open('historic.json', 'w') as outfile:
                json.dump(reqs, outfile,indent=4,ensure_ascii=False)

            #print("BREAK 12")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            print("wrong token")
            return jsonify(invalid_msg), 401

    return _verify

def admin_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
            query = f'match (n:User) where n._id = "{data["sub"]}" AND n.tipo = "Admin" return n'
            user = neo4j_db.evaluate(query)
            now = datetime.datetime.now()
            ''' date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            did = ObjectId()
            reqstring= request.method + ":" + request.url '''
            if not user:
                raise RuntimeError('User or Administrator not found')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

def photo_auth(request, picName):
    auth_headers = request.headers.get('Authorization', '').split()

    token = auth_headers[1]
    #data = jwt.decode(token, current_app.config['SECRET_KEY'])
    data = jwt.decode(token,'\t\xcf\xbb\xe6~\x01\xdf4\x8b\xf3?i')
    query = f'match (n:User) where n._id = "{data["sub"]}" AND n.tipo = "Admin" return n'
    user = neo4j_db.evaluate(query)
    if user:
        if user['tipo'] == 'Admin':
            return True
        elif user['_id'] == picName:
            return True
    return False

