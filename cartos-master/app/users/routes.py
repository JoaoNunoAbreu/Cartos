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


@blueprint.route('/users', methods=['GET'])
@admin_required
#@token_required
#@login_required
def route_users():
    """
    Consultar Utilizadores.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true


    responses:
      200:
        description: Lista de Utilizadores.
        schema:
          type: array
          items:
            $ref: '#/definitions/Utilizador'
    """
    
    users = neo4j_db.run('match (x:User) return x')
    return json_util.dumps(users.data())


###########################################
@blueprint.route('/foto/<user>', methods=['GET'])
@token_required
def route_photo(user):
    """
    Consultar a imagem de perfil de um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - in: formData
        name: foto
        type: file
        required: true

      - in: path
        name: user
        type: string
        required: true

    produces:
      - image/png
    responses:
      200:
        description: Foto do Utilizador.
    """

    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, user)
    if photo_auth (request, user) and path.exists(pathCheck) :
        return send_from_directory(pathPhoto, user, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')

@blueprint.route('/foto/atualizar/<user>', methods=['POST'])
@token_required
def route_foto_atualizar(user):
    """
    Atualizar a imagem de perfil de um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - name: user
        in: user
        type: string
        required: true

      - in: formData
        name: foto
        type: file
        required: true

    produces:
      - image/png
    responses:
      200:
        description: Ok, se o pedido for efetuado.
    """

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
def route_cur(user):
    """
    Consultar o curriculo de perfil de um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - name: user
        in: user
        type: string
        required: true

    produces:
        - application/pdf
    responses:
      200:
        description: PDF correspondente ao curriculo do utilizador.
        schema:
          type: file
    """

    pathC = join(dirname(realpath(__file__)), 'static/curriculo/')
    pathCheck = join(pathC, user)
    if photo_auth(request, user) and path.exists(pathCheck):    
        return send_from_directory(pathC, user,mimetype='application/pdf')
    else:
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')

@blueprint.route('/curriculo/atualizar/<user>', methods=['POST'])
@token_required
def route_cur_atualizar(user):
    """
    Atualizar o curriculo de perfil de um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - name: user
        in: user
        type: string
        required: true

      - in: formData
        name: curriculo
        type: file
        required: true

    produces:
        - application/pdf
    responses:
      200:
        description: PDF atualizado.
        schema:
          type: file
    """
    
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

@blueprint.route('/apagar/<user>')
@admin_required
#@login_required
def route_template_apagar(user):
    """
    Apagar um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - name: user
        in: user
        type: string
        required: true

    responses:
      200:
        description: Utilizador removido.
        schema:
          $ref: '#/definitions/Utilizador'
    """

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
#@login_required
def route_template_editar_guardar():
    """
    Guardar Template Editado.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    
      - in: formData
        name: username
        type: string

      - in: formData
        name: name
        type: string

      - in: formData
        name: email
        type: string

      - in: formData
        name: tipo
        type: string

      - in: formData
        name: universidade
        type: string

      - in: formData
        name: departamento
        type: string

      - in: formData
        name: obs
        type: string
        
    responses:
      200:
        description: Change.
        schema:
          type: string
    """
    username = request.form.get('username')
    nome = request.form.get('name')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    universidade = request.form.get('universidade')
    departamento = request.form.get('departamento')
    obs = request.form.get('obs')
    if(username == None):
      username = ""
    if(nome == None):
      nome = ""
    if(email == None):
      email = ""
    if(tipo == None):
      tipo = ""
    if(universidade == None):
      universidade = ""
    if(departamento == None):
      departamento = ""
    if(obs == None):
      obs = ""
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

    neo4j_db.run(f'MATCH (n:User {{_id: "{username}"}}) SET n += {{nome: "{nome}",email: "{email}", tipo: "{tipo}",universidade: "{universidade}",departamento: "{departamento}",obs: "{obs}" }} RETURN n')
    users = neo4j_db.run('match (x:User) return x')
    return json_util.dumps({'users': users})

@blueprint.route('/registar', methods=['POST'])
#@admin_required
#@login_required
def route_template_registar_pedido():
    """
    Efetuar um pedido de resgisto.
    ---
    parameters:
      - in: formData
        name: foto
        type: file
        
      - in: formData
        name: curriculo
        type: file

      - in: formData
        name: username
        type: string
        required: true

      - in: formData
        name: name
        type: string
        required: true

      - in: formData
        name: password
        type: string
        required: true

      - in: formData
        name: email
        type: string
        required: true

      - in: formData
        name: tipo
        type: string
        required: true

      - in: formData
        name: universidade
        type: string

      - in: formData
        name: departamento
        type: string

      - in: formData
        name: obs
        type: string

    definitions:
      PedidoRegistar:
        type: object
        properties:
          nome:
            type: string
            description: Nome do Utilizador.

    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/PedidoRegistar'
    """
    
    username = request.form.get('username')
    existeU = neo4j_db.evaluate('match (x:User) where x.username=$v return x',v=username)

    nome = request.args.get('nome')
    if existeU:
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


@blueprint.route('/active', methods=['GET'])
@token_required
def route_active():
    """
    Ativar conta de um respetivo utilizador.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

    definitions:
      UtilizadoresAtivos:
        type: object
        properties:
          nome:
            type: array
            items:
              $ref: '#/definitions/Utilizador'
            description: Array de Utilizadores.

    responses:
      200:
        description: Lista de utilizadores ativos.
        schema:
          $ref: '#/definitions/UtilizadoresAtivos'
    """
    
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
def route_history():
    """
    Consultar Histórico.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

    responses:
      200:
        description: Histórico.
        schema:
          type: array
          items:
            type: string
    """
    with open('historic.json') as json_file:
        reqs = json.load(json_file)
    return json_util.dumps({'reqs': reqs})


@blueprint.route('/historyCleanse', methods=['GET'])
@token_required
def route_historyCleanse():
    """
    Limpar Histórico.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

    responses:
      200:
        description: Histórico Limpo.
        schema:
          type: array
          items:
            type: string
    """
    with open('historic.json', 'w') as outfile:
        json.dump([], outfile)
    return json_util.dumps({'history': [] })
