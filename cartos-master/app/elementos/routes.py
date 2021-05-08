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
        data.append({
            "id":elem[0]['id'] ,
            "data_publicacao":elem[0]['data_publicacao'], 
            "colecao":colecao,
            "editora":editora,
            "lingua":lingua
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
    print (pathC)
    if path.exists(pathC) :    
        return send_from_directory(pathC, f ,mimetype='application/pdf')
    else :
        return send_from_directory(pathC, "blank.pdf",mimetype='application/pdf')



@blueprint.route('/remover/<folio>')
@admin_required
#@login_required
def route_template_remover(folio):
    nome = request.args.get('nome')
    existe = mongo.db.folios.find_one({"_id":folio})
    return render_template('removerElemento.html', folio=existe,nome=nome)

@blueprint.route('/apagar/<folio>', methods=['GET'])
@admin_required
#@login_required
def route_template_apagar(folio):
    indices = mongo.db.indexacao.find()
    for indice in indices:
        if(folio in indice['ref']):
            if(len(indice['ref']) == 1):
                mongo.db.indexacao.remove({"_id":indice['_id']})
            else:
                indice['ref'].remove(folio)
                array = indice['ref']
                ocorrencias = indice['ocorrencias']
                index = 0
                for oco in ocorrencias:
                    for key in oco:
                        if(key == folio):
                            tamanho = len(oco[key])
                            index_remove = index
                            lista = ocorrencias.pop(index_remove)
                            valor = indice['n_ocorrencias'] - tamanho
                            mongo.db.indexacao.remove({"_id":indice['_id']})
                            novo = {
                                "_id":indice['_id'],
                                "ocorrencias": lista,
                                "ref":array,
                                "n_ocorrencias":valor
                            }   
                            mongo.db.indexacao.insert(novo)
    tags = mongo.db.tags.find()
    for tag in tags:
        if(folio in tag['ref']):
            if(len(tag['ref']) == 1):
                mongo.db.tags.remove({"_id":tag['_id']})
            else:
                tag['ref'].remove(folio)
                array = tag['ref']
                ocorrencias = tag['conteudoTag']
                index = 0
                for oco in ocorrencias:
                    for key in oco:
                        if(key == folio):
                            tamanho = len(oco[key])
                            index_remove = index
                            lista = ocorrencias.pop(index_remove)
                            valor = tag['n_ocorrencias'] - tamanho
                            mongo.db.tags.remove({"_id":tag['_id']})
                            novo = {
                                "_id":tag['_id'],
                                "conteudoTag": lista,
                                "ref":array,
                                "n_ocorrencias":valor
                            }
                            mongo.db.tags.insert(novo)
    removeu = mongo.db.folios.remove({"_id":folio})
    folio_filename = str(folio) + ".txt"
    foto_filename = str(folio)
    remove_path = join(dirname(realpath(__file__)), 'static/doc/', folio_filename)
    if path.exists(remove_path):
        remove(remove_path)
    foto_remove_path = join(dirname(realpath(__file__)), 'static/pics/', foto_filename)
    if path.exists(foto_remove_path):
        remove(foto_remove_path) 
    nome = request.args.get('nome')
    folios = [doc for doc in mongo.db.folios.find()]
    return json_util.dumps({'folios': folios, 'nome': nome})


############################### INDICES #########################################

@blueprint.route('/index', methods=['GET'])
@token_required
#@login_required
def route_template_index():
    nome = request.args.get('nome')
    index = mongo.db.indexacao.find()
    return json_util.dumps({'indexs':index, 'nome':nome})

@blueprint.route('/index/ver/<indice>', methods=['GET'])
@token_required
#@login_required
def route_template_index_ver(indice):
    nome = request.args.get('nome')
    existe = mongo.db.indexacao.find_one({"_id":indice})
    print(existe)
    return render_template('viewIndex.html', index=existe,nome=nome)


############################### Tags #########################################

@blueprint.route('/tags', methods=['GET'])
@token_required
#@login_required
def route_template_tags():
    tags = mongo.db.tags.find()
    nome = request.args.get('nome')
    return json_util.dumps({'tags':tags, 'nome':nome})

@blueprint.route('/tags/ver/<tag>', methods=['GET'])
@token_required
#@login_required
def route_template_tag_ver(tag):
    nome = request.args.get('nome')
    existe = mongo.db.tags.find_one({"_id":tag})
    return render_template('viewTag.html', tag=existe,nome=nome)

############################### Pesquisas ###################################

@blueprint.route('/pesquisas', methods=['GET'])
@admin_required
def route_pesquisas():
    pesquisas= [doc for doc in mongo.db.pesquisas.find()]
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
