#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.elementos import blueprint
from flask import render_template, request, url_for, send_from_directory
from flask_login import login_required
from app import token_required, admin_required, photo_auth, neo4j_db
from os import path, remove, listdir
from os.path import join, dirname, realpath
from werkzeug.security import generate_password_hash

###### new imports
import datetime
import json 
import os    
from bson import json_util
from flasgger import swag_from
from flask_cors import CORS, cross_origin
CORS(blueprint)
######

############################### ELEMENTOS #########################################

@blueprint.route('/elementos', methods=['GET'])
#@token_required
#@login_required
@swag_from('docs/elementos-get.yml')
def route_template_elementos():

    elementos = neo4j_db.run('match (x:Elemento) return x')
  
    data = [ ]
    for elem in elementos:
        colecao = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Colecao) where e.id="{elem[0]["id"]}" return c.designacao')
        editora = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Editora) where e.id="{elem[0]["id"]}" return c.designacao')
        lingua = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Lingua) where e.id="{elem[0]["id"]}" return c.designacao')
        tipo = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Tipo) where e.id="{elem[0]["id"]}" return c.designacao')
        data.append({
            "id":elem[0]['id'] ,
            "titulo":elem[0]['titulo'] ,
            "capa": elem[0]['capa'],
            "estado": elem[0]['estado'],
            "numero": elem[0]['numero'],
            "nr_paginas": elem[0]['nr_paginas'],
            "texto": elem[0]['texto'],
            "observacoes": elem[0]['observacoes'],
            "tamanho": elem[0]['tamanho'],
            "personagens": elem[0]['personagens'],
            "serie": elem[0]['serie'],
            "data_publicacao":elem[0]['data_publicacao'],
            "colecao":colecao,
            "editora":editora,
            "lingua":lingua,
            "tipo": tipo
        }) 
    return json_util.dumps(data)

@blueprint.route('/<elemento>', methods=['GET'])
@swag_from('docs/elemento-get.yml')
def route_template_elemento(elemento):

    el = neo4j_db.evaluate(f'match (x:Elemento) where x.id="{elemento}" return x')
    data = [ ]
    colecao = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Colecao) where e.id="{el["id"]}" return c.designacao')
    editora = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Editora) where e.id="{el["id"]}" return c.designacao')
    lingua = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Lingua) where e.id="{el["id"]}" return c.designacao')
    tipo = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Tipo) where e.id="{el["id"]}" return c.designacao')
    data.append({
        "id":el['id'] ,
        "titulo":el['titulo'] ,
        "capa": el['capa'],
        "estado": el['estado'],
        "numero": el['numero'],
        "nr_paginas": el['nr_paginas'],
        "texto": el['texto'],
        "observacoes": el['observacoes'],
        "tamanho": el['tamanho'],
        "personagens": el['personagens'],
        "serie": el['serie'],
        "data_publicacao":el['data_publicacao'],
        "colecao":colecao,
        "editora":editora,
        "lingua":lingua,
        "tipo": tipo
    })
    return json_util.dumps(data)

@blueprint.route('/editoras', methods=['GET'])
@swag_from('docs/editoras-get.yml')
def route_template_editoras():

    editoras = neo4j_db.run('match (x:Editora) return x')
    return json_util.dumps(editoras)

@blueprint.route('/colecoes', methods=['GET'])
@swag_from('docs/colecoes-get.yml')
def route_template_colecoes():

    colecoes = neo4j_db.run('match (x:Colecao) return x')
    return json_util.dumps(colecoes)

@blueprint.route('/linguas', methods=['GET'])
@swag_from('docs/linguas-get.yml')
def route_template_linguas():

    linguas = neo4j_db.run('match (x:Lingua) return x')
    return json_util.dumps(linguas)

@blueprint.route('/tipos', methods=['GET'])
@swag_from('docs/tipos-get.yml')
def route_template_tipo():

    tipos = neo4j_db.run('match (x:Tipo) return x')
    return json_util.dumps(tipos)


@blueprint.route('/ver/<elemento>/foto', methods=['GET'])
#@token_required
#@login_required
@swag_from('docs/ver-elemento-foto-get.yml')
def route_template_ver_foto(elemento):

    f = elemento + ".png"
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, f)
    if path.exists(pathCheck) :
        return send_from_directory(pathPhoto, f, mimetype='image/*')
    else :
        return send_from_directory(pathPhoto, "default.jpg", mimetype='image/png')

@blueprint.route('/ver/<elemento>/video', methods=['GET'])
#@token_required
#@login_required
@swag_from('docs/ver-elemento-video-get.yml')
def route_template_ver_video(elemento):

    f = elemento + ".mp4"
    pathVideo = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathVideo, f)
    if path.exists(pathCheck) :
        return send_from_directory(pathVideo, f, mimetype='video/mp4')
    else:
        return json_util.dumps({"message":"Sem vídeo."})

@blueprint.route('/ver/<elemento>/ficheiro', methods=['GET'])
@swag_from('docs/ver-elemento-ficheiro-get.yml')
def route_template_ver_ficheiro(elemento):

    pathC = join(dirname(realpath(__file__)), 'static/doc/')
    f = elemento + ".pdf"
    pathCheck = join(pathC, f)
    if path.exists(pathCheck) :    
        return send_from_directory(pathC, f ,mimetype='application/pdf')
    else:
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')

@blueprint.route('/apagar/<elemento>', methods=['GET'])
@admin_required
#@login_required
@swag_from('docs/apagar-elemento-get.yml')
def route_template_apagar(elemento):

    q = f'MATCH (n:Elemento)-[r]-() where n.id="{elemento}" DELETE r'
    neo4j_db.run(q)

    q = f'MATCH (n:Elemento) WHERE n.id = "{elemento}" DELETE n'
    neo4j_db.run(q)

    elemento_filename = str(elemento) + ".pdf"
    foto_filename = str(elemento)
    remove_path = join(dirname(realpath(__file__)), 'static/doc/', elemento_filename)
    if path.exists(remove_path):
        remove(remove_path)

    pics = join(dirname(realpath(__file__)), 'static/pics/') 
    deleteIfFotoVideoExists(pics,foto_filename)

    # -----------------------------

    elementos = neo4j_db.run('match (x:Elemento) return x')
    data = []
    for elem in elementos:
        colecao = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Colecao) where e.id="{elem[0]["id"]}" return c.designacao')
        editora = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Editora) where e.id="{elem[0]["id"]}" return c.designacao')
        lingua = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Lingua) where e.id="{elem[0]["id"]}" return c.designacao')
        data.append({
            "id":elem[0]['id'] ,
            "data_publicacao":elem[0]['data_publicacao'], 
            "colecao":colecao,
            "editora":editora,
            "lingua":lingua
        }) 
    return json_util.dumps(data)

def deleteIfFotoVideoExists(pics,file):
  l = os.listdir(pics)
  li = [x.split('.')[0] for x in l]
  if (file in li):
    remove = join(pics,file)
    remove(remove)
