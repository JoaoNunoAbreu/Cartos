#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.users import blueprint
from flask import render_template, request, flash, send_from_directory
from flask_login import login_required
from app import token_required, admin_required, photo_auth, neo4j_db
from os import path, remove, rename, replace
from werkzeug.security import generate_password_hash
import datetime
import os
from os.path import join, dirname, realpath
from shutil import copyfile, move
###### este é meu
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######
UPLOAD_FOLDER = './static/pics/'

from flasgger import swag_from
@blueprint.route('/users', methods=['GET'])
@admin_required
#@token_required
#@login_required
@swag_from('docs/users.yml')
def route_users():
    users = neo4j_db.run('match (x:User) return x')
    return json_util.dumps(users.data())


@blueprint.route('/adicionar')
@admin_required
#@login_required
@swag_from('docs/adicionar.yml')
def route_template_adicionar():
    nome = request.args.get('nome')
    return render_template('registar.html',nome=nome)


@blueprint.route('/ver/<user>', methods=['GET'])
@admin_required
#@login_required
@swag_from('docs/ver-user-get.yml')
def route_template_ver(user):

    nome = request.args.get('nome')
    existe = neo4j_db.evaluate('match (x:User) where x._id=$v return x',v=username)
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    if path.exists(upload_path2):
        curriculo = user
    else:
        curriculo = "default.png"
    return json_util.dumps({'user': existe, 'foto':upload_path, 'curriculo':upload_path2, 'nome':nome})



###########################################
@blueprint.route('/foto/<user>', methods=['GET'])
@token_required
@swag_from('docs/foto-user-get.yml')
def route_photo(user):

    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if photo_auth (request, user) and path.exists(pathCheck) :
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

@blueprint.route('/foto/atualizar/<user>', methods=['POST'])
@token_required
@swag_from('docs/foto-atualizar-user-post.yml')
def route_foto_atualizar(user):

    if 'foto' in request.files:
        foto = request.files['foto']
        upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
        if path.exists(upload_path): 
            remove(upload_path)
        if foto.filename != '':
            foto.filename = user
            upload_path2 = join(dirname(realpath(__file__)), 'static/pics/')
            foto.save(upload_path2 + foto.filename)
        else:
            src = join(dirname(realpath(__file__)), 'static/pics/', user + ".png") 
            upload_path2 = join(dirname(realpath(__file__)), 'static/pics/', user + ".png")
            copyfile(src, upload_path2)

    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if photo_auth (request, user) and path.exists(pathCheck) :
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')



##########################################
@blueprint.route('/curriculo/<user>', methods=['GET'])
@token_required
@swag_from('docs/curriculo-user-get.yml')
def route_cur(user):

    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
    pathCheck = join(pathC, user)
    if photo_auth(request, user) and path.exists(pathCheck):    
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else:
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')

@blueprint.route('/curriculo/atualizar/<user>', methods=['POST'])
@token_required
@swag_from('docs/curriculo-atualizar-user-post.yml')
def route_cur_atualizar(user):
    
    if 'curriculo' in request.files:
        curriculo = request.files['curriculo']
        upload_path = join(dirname(realpath(__file__)), 'static/curriculo/', user)
        if path.exists(upload_path): 
            remove(upload_path)
        if curriculo.filename != '':
            curriculo.filename = user
            upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/')
            curriculo.save(upload_path2 + curriculo.filename)
        else:
            src = join(dirname(realpath(__file__)), 'static/curriculo/', user + ".pdf") 
            upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user + ".pdf")
            copyfile(src, upload_path2)

    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
    if photo_auth (request, user) :
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')
##########################################



@blueprint.route('/editar/<user>')
@admin_required
#@login_required
@swag_from('docs/editar-user.yml')
def route_template_editar(user):
    
    existe = neo4j_db.evaluate('match (x:User) where x._id=$v return x',v=user)
    nome = request.args.get('nome')
    return json_util.dumps({'user': existe, 'nome': nome})


@blueprint.route('/remover/<user>')
@admin_required
#@login_required
@swag_from('docs/remover-user.yml')
def route_template_remover(user):
    
    nome = request.args.get('nome')
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    if path.exists(upload_path):
        foto = user
    else:
        foto = "default.png"
    return render_template('remover.html',user=user,foto=foto,nome=nome)


@blueprint.route('/apagar/<user>')
@admin_required
#@login_required
@swag_from('docs/apagar-user.yml')
def route_template_apagar(user):

    neo4j_db.evaluate('match (x:User) where x._id=$v delete x',v=user)
    upload_path = join(dirname(realpath(__file__)), 'static/pics/', user)
    upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', user)
    if path.exists(upload_path): 
        remove(upload_path)
    if path.exists(upload_path2): 
        remove(upload_path2)
    users = neo4j_db.run('match (x:User) return x').data()
    data = [i['x'] for i in users]
    return json_util.dumps(data)

@blueprint.route('/editar/guardar', methods=['POST'])
@admin_required
@swag_from('docs/editar-guardar-post.yml')
#@login_required
def route_template_editar_guardar():

    username = request.form.get('username')
    nome = request.form.get('name')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    universidade = request.form.get('universidade')
    departamento = request.form.get('departamento')
    obs = request.form.get('obs')
    if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
    if 'curriculo' in request.files:
            curriculo = request.files['curriculo']
            if curriculo.filename != '':
                curriculo.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/curriculo/')
                curriculo.save(upload_path + curriculo.filename)
    password = request.form.get('password')

    if password:    
        neo4j_db.run(f'MATCH (n:User {{_id: "{username}"}}) SET n += {{nome: "{nome}",email: "{email}",password:"{password}", tipo: "{tipo}",universidade: "{universidade}",departamento: "{departamento}",obs: "{obs}" }} RETURN n')
    else:
        neo4j_db.run(f'MATCH (n:User {{"_id": "{username}"}}) SET n += {{nome: "{nome}",email: "{email}", tipo: "{tipo}",universidade: "{universidade}",departamento: "{departamento}",obs: "{obs}" }} RETURN n')
    users = neo4j_db.run('match (x:User) return x')
    return json_util.dumps({'users': users})

###### PEDIDOS ######

@blueprint.route('/pedidos/registar', methods=['POST'])
#@admin_required
#@login_required
@swag_from('docs/pedidos-registar-post.yml')
def route_template_registar_pedido():

    username = request.form.get('username')
    existeU = neo4j_db.evaluate('match (x:User) where x.username=$v return x',v=username)
    existeP = neo4j_db.evaluate('match (x:Pedidos) where x.username=$v return x',v=username)

    nome = request.args.get('nome')
    if existeU or existeP:
        #flash('ERRO: Username já escolhido. Por favor escolha outro...')
        #return render_template('registar.html',nome=nome)
        return json_util.dumps({'nome': nome,'message':'já existe'})
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        encryptPass = generate_password_hash(password)
        tipo = request.form.get('tipo')
        universidade = request.form.get('universidade')
        departamento = request.form.get('departamento')
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d %H:%M")
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                foto.filename = username
                upload_path = join(dirname(realpath(__file__)), 'static/pics/')
                foto.save(upload_path + foto.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/pics/', username + ".png") 
                upload_path = join(dirname(realpath(__file__)), 'static/pics/', username + ".png")
                copyfile(src, upload_path)
        if 'curriculo' in request.files:
            curriculo = request.files['curriculo']
            if curriculo.filename != '':
                curriculo.filename = username
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/')
                curriculo.save(upload_path2 + curriculo.filename)
            else:
                src = join(dirname(realpath(__file__)), 'static/curriculo/', username + ".pdf") 
                upload_path2 = join(dirname(realpath(__file__)), 'static/curriculo/', username + ".pdf")
                copyfile(src, upload_path)
        obs = request.form.get('obs')
        neo4j_db.run('CREATE (n:User{_id:$username,nome:$name,email:$email,password:$password,tipo:$tipo,universidade:$universidade,departamento:$departamento,data:$data,obs:$obs})',
            username=username,
            name=name,
            email=email,
            password=encryptPass,
            tipo=tipo,
            universidade=universidade,
            departamento=departamento,
            data=data,
            obs=obs
        )
        return json_util.dumps({'nome': nome})



###########################################
@blueprint.route('/pedidos/foto/<pedido>', methods=['GET'])
@token_required
@swag_from('docs/pedidos-foto-pedido-get.yml')
def route_photo_pedido(pedido):

    pathPhoto = join(dirname(realpath(__file__)), 'static/picsPedidos/')
    pathCheck = join(pathPhoto, pedido)
    if photo_auth (request, pedido) and path.exists(pathCheck) :  
        return send_from_directory(pathPhoto, pedido, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

##########################################
@blueprint.route('/pedidos/curriculo/<pedido>', methods=['GET'])
@token_required
@swag_from('docs/pedidos-curriculo-pedido-get.yml')
def route_cur_pedido(pedido):

    pathC = join(dirname(realpath(__file__)), 'static/curriculoPedidos/')
    print (pathC)
    print (pedido)
    if photo_auth (request, pedido) :    
        return send_from_directory(pathC, pedido,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "Rafiki",mimetype='application/pdf')
##########################################


@blueprint.route('/active', methods=['GET'])
@token_required
@swag_from('docs/active-get.yml')
def route_active():

    users = neo4j_db.run('match (x:User) where x.ativo="true" return x').data()
    date = datetime.datetime.now()
    date = date - datetime.timedelta(minutes = 15)
    ret=[]
    
    for u in users:
        if datetime.datetime.strptime(u['x']['stamp'],'%Y-%m-%d %H:%M:%S.%f') > date :
            ret.append(u['x'])
    return json_util.dumps({'users': ret})
    #return render_template('users.html',users=users,nome=nome)


@blueprint.route('/history', methods=['GET'])
@token_required
@swag_from('docs/history-get.yml')
def route_history():
    with open('historic.json') as json_file:
        reqs = json.load(json_file)
    return json_util.dumps({'reqs': reqs})


@blueprint.route('/historyCleanse', methods=['GET'])
@token_required
@swag_from('docs/historyCleanse-post.yml')
def route_historyCleanse():
    with open('historic.json', 'w') as outfile:
        json.dump([], outfile)
    return json_util.dumps({'history': [] })
