#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.elementos import blueprint
from flask import render_template, request, url_for, send_from_directory
from flask_login import login_required
from app import mongo, token_required, admin_required, photo_auth, neo4j_db
from os import path, remove, listdir
from os.path import join, dirname, realpath
from werkzeug.security import generate_password_hash

###### new imports
import datetime
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######

############################### ELEMENTOS #########################################

@blueprint.route('/elementos', methods=['GET'])
@token_required
#@login_required
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
def route_template_editoras():
    editoras = neo4j_db.run('match (x:Editora) return x')
    return json_util.dumps(editoras)

@blueprint.route('/colecoes', methods=['GET'])
def route_template_colecoes():
    colecoes = neo4j_db.run('match (x:Colecao) return x')
    return json_util.dumps(colecoes)

@blueprint.route('/linguas', methods=['GET'])
def route_template_linguas():
    linguas = neo4j_db.run('match (x:Lingua) return x')
    return json_util.dumps(linguas)

@blueprint.route('/tipos', methods=['GET'])
def route_template_tipo():
    tipos = neo4j_db.run('match (x:Tipo) return x')
    return json_util.dumps(tipos)


@blueprint.route('/ver/<elemento>/foto', methods=['GET'])
#@token_required
#@login_required
def route_template_ver_foto(elemento):
    f = "RP" + ".png"
    pathPhoto = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathPhoto, f)
    if path.exists(pathCheck) :
        return send_from_directory(pathPhoto, f, mimetype='image/png')
    else :
        return send_from_directory(pathPhoto, "default", mimetype='image/png')


@blueprint.route('/ver/<elemento>/ficheiro', methods=['GET'])
def route_template_ver_ficheiro(elemento):
    pathC = join(dirname(realpath(__file__)), 'static/doc/')
    f = elemento + ".pdf"
    if path.exists(pathC) :    
        return send_from_directory(pathC, f ,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')

@blueprint.route('/apagar/<elemento>', methods=['GET'])
@admin_required
#@login_required
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
    foto_remove_path = join(dirname(realpath(__file__)), 'static/pics/', foto_filename)
    if path.exists(foto_remove_path):
        remove(foto_remove_path) 

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

############################### Pesquisas ###################################

@blueprint.route('/pesquisas', methods=['GET'])
@admin_required
def route_pesquisas():
    pesquisas = [doc for doc in mongo.db.pesquisas.find()]
    nome = request.args.get('nome')
    return json_util.dumps({'pesquisas': pesquisas, 'nome': nome})

@blueprint.route('/compElementos/pesquisas', methods=['GET'])
@admin_required
def route_pesquisasCompElementos():
    nome = request.args.get('nome')
    pesquisas= [doc for doc in mongo.db.pesquisasCF.find({"username":nome})]
    return json_util.dumps({'pesquisas': pesquisas, 'nome': nome})

@blueprint.route('/compElementos/post', methods=['POST'])
@token_required
#@login_required
def route_pesquisasPost():
    pesquisa = request.form.get('pesquisa')
    username = request.form.get('username')
    now = datetime.datetime.now()
    data = now.strftime("%Y-%m-%d %H:%M")
    value = mongo.db.pesquisasCF.insert({"pesquisa":pesquisa,"data":data,"username":username})
    pesquisas= [doc for doc in mongo.db.pesquisasCF.find({"username":username})]
    nome = request.args.get('nome')
    return json_util.dumps({'pesquisas': pesquisas, 'nome': nome})
