#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.importacao import blueprint
from flask import render_template,request,flash,redirect,url_for, send_from_directory
from flask_login import login_required
from app import mongo,dadosFolio,indexList,tags, token_required, admin_required
from app.indexador import indexacao as index, extractor as extract
import datetime
import os
from os.path import join, dirname, realpath
###### este é meu
import json 
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
#######
UPLOAD_FOLDER = '../folios/static/pics/'


@blueprint.route('/passo1/',methods=['POST'])
@admin_required
#@login_required
def route_template_passo1():
    if request.method == 'POST':
        folio = mongo.db.folios.find_one({"_id": request.form.get('idFolio')})
        nome = request.args.get('nome')
        if folio:
            flash('Este id já existe')
            return json_util.dumps({'nome': nome,'message':'O ID do Fólio já existe.'})
        else:
            if 'ficheiro' in request.files:
                ficheiro = request.files['ficheiro']
                if ficheiro.filename == '':
                    return json_util.dumps({'nome': nome,'message':'O Fólio não possui ficheiro.'})
                else:
                    ficheiro.filename = request.form.get('idFolio') + '.txt'
                    path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', ficheiro.filename)
                    ficheiro.save(path)
                    tags = []
                    indexList = []
                    tags = extract.extraiTags(path)
                    indexList = index.indexFile(path)
                    textoTags = extract.extraiTexto(path)
                    textoSTags = extract.extraiTextoSTags(path)
                    temp = extract.getInfo(path,tags,indexList)
                    os.remove(path)
                    return json_util.dumps({'nome': nome,'message':'não existe','textoTags':textoTags,'textoSTags':textoSTags,'tags':tags,'list':indexList,'passo6':temp})

@blueprint.route('/passo6/',methods=['POST'])
@admin_required
#@login_required
def route_template_passo6():

    """ nome = request.args.get('nome')
    if 'ficheiro' in request.files:
        ficheiro = request.files['ficheiro']
        if ficheiro.filename == '':
            flash('Não submeteu nenhum Ficheiro')
            return json_util.dumps({'nome': nome, 'message':'nao correu bem'})
        else:
            ficheiro.filename = request.form.get('idFolio') + '.txt'
            path = join(dirname(realpath(__file__)), '..', 'folios/static/doc', ficheiro.filename)
            ficheiro.save(path)
            tags = []
            indexList = []
            tags = extract.extraiTags(path)
            indexList = index.indexFile(path)
    if 'foto' in request.files:
        foto = request.files['foto']
        if foto.filename != '':
            foto.filename = request.form.get('idFolio')
            upload_path = join(dirname(realpath(__file__)),'..' ,'folios/static/pics/')
            foto.save(upload_path + foto.filename + '.png')
    now = datetime.datetime.now()
    data = now.strftime("%Y-%m-%d %H:%M")
    if 'observacao' in dadosFolio.keys():
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"tipo":request.form.get('tipo'),"observacao":request.form.get('obs'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data,"user":request.args.get('nome')})
    else:
        mongo.db.folios.insert({"_id":request.form.get('idFolio'),"descricao":request.form.get('descricao'),"tipo":request.form.get('tipo'),"versao":request.form.get('versao'),'sumario':request.form.get('sumario'),"textoCTags":request.form.get('textoTags'),"textoSTags":request.form.get('textoSTags'),"data":data,"user":request.args.get('nome')})
    for l in indexList:
        indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
        if indice:
            n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
            ocorrencias = []
            for i in indice["ocorrencias"]:
                ocorrencias.append(i)
            for i in l["ocorrencias"]:
                newDict = {}
                newDict[i] = l["ocorrencias"][i]
                ocorrencias.append(newDict)
            ref = []
            for i in indice["ref"]:
                ref.append(i)
            for i in l["ref"]:
                ref.append(i)
            mongo.db.indexacao.find_one_and_update({"_id": l["_id"]},{"$set": {"n_ocorrencias":n_ocorrencias,"ocorrencias":ocorrencias,"ref":ref}})
        else:
            ocorrencias = []
            ocorrencias.append(l["ocorrencias"])
            mongo.db.indexacao.insert_one({"_id":l["_id"],"n_ocorrencias":l["n_ocorrencias"],"ocorrencias":ocorrencias,"ref":l["ref"]})
    n_ocorrencias = 0
    for t in tags:
        tag = mongo.db.tags.find_one({"_id":t["tag"]})
        if tag:
            n_ocorrencias = tag["n_ocorrencias"]+t["n_ocorrencias"]
            ref = []
            for i in tag["ref"]:
                ref.append(i)
            for i in t["ref"]:
                ref.append(i)
            conteudo = []
            for i in tag["conteudoTag"]:
                conteudo.append(i)
            for i in t["conteudoTag"]:
                conteudo.append(i)
            mongo.db.tags.find_one_and_update({"_id": t["tag"]},{"$set":{"n_ocorrencias":n_ocorrencias,"ref":ref,"conteudoTag":conteudo}})
        else:
            mongo.db.tags.insert_one({"_id":t["tag"],"n_ocorrencias":t["n_ocorrencias"],"ref":t["ref"],"conteudoTag":t["conteudoTag"]})
    """
    print("\n\n\nola\n\n\n")
    return json_util.dumps({'pixa': "pixa"})

    #return json_util.dumps({'nome': nome, 'message':'inserido com sucesso'})

@blueprint.route('/reindex/',methods=['GET'])
@admin_required
#@login_required
def route_template_reindex():
    mongo.db.indexacao.drop()
    textos = [doc for doc in mongo.db.folios.find({},{'textoSTags':1})] 
    for texto in textos:
        lista = []
        lista = index.indexDB(texto['textoSTags'],texto['_id'])
        for l in lista:
            indice = mongo.db.indexacao.find_one({"_id":l["_id"]})
            if indice:
                n_ocorrencias = indice["n_ocorrencias"] + l["n_ocorrencias"]
                ocorrencias = []
                for i in indice["ocorrencias"]:
                    ocorrencias.append(i)
                for i in l["ocorrencias"]:
                    newDict = {}
                    newDict[i] = l["ocorrencias"][i]
                    ocorrencias.append(newDict)
                ref = []
                for i in indice["ref"]:
                    ref.append(i)
                for i in l["ref"]:
                    ref.append(i)
                mongo.db.indexacao.find_one_and_update({"_id": l["_id"]},{"$set": {"n_ocorrencias":n_ocorrencias,"ocorrencias":ocorrencias,"ref":ref}})
            else:
                ocorrencias = []
                ocorrencias.append(l["ocorrencias"])
                mongo.db.indexacao.insert_one({"_id":l["_id"],"n_ocorrencias":l["n_ocorrencias"],"ocorrencias":ocorrencias,"ref":l["ref"]})
    return json_util.dumps({'message':'ok'})
