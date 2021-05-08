#!/usr/bin/python
# -*- coding: utf-8 -*-

from app.importacao import blueprint
from flask import render_template,request,flash,redirect,url_for, send_from_directory
from flask_login import login_required
from app import mongo,indexList,tags, token_required, admin_required, neo4j_db
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
UPLOAD_FOLDER = '../elementos/static/pics/'

@blueprint.route('/passo1/',methods=['POST'])
@admin_required
#@login_required
def route_template_passo1():
    if request.method == 'POST':
        folio = mongo.db.folios.find_one({"_id": request.form.get('idElemento')})
        nome = request.args.get('nome')
        if folio:
            flash('Este id já existe')
            return json_util.dumps({'nome': nome,'message':'O ID do Elemento já existe.'})
        else:
            if 'ficheiro' in request.files:
                ficheiro = request.files['ficheiro']
                if ficheiro.filename == '':
                    return json_util.dumps({'nome': nome,'message':'O Elemento não possui ficheiro.'})
                else:
                    ficheiro.filename = request.form.get('idElemento') + '.txt'
                    path = join(dirname(realpath(__file__)), '..', 'elementos/static/doc', ficheiro.filename)
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

    nome = request.args.get('nome')
    path = ""
    capa = ""

    if 'ficheiro' in request.files:
        ficheiro = request.files['ficheiro']
        if ficheiro.filename == '':
            flash('Não submeteu nenhum Ficheiro')
            return json_util.dumps({'nome': nome, 'message':'nao correu bem'})
        else:
            ficheiro.filename = request.form.get('id') + '.pdf'
            path = join(dirname(realpath(__file__)), '..', 'elementos/static/doc', ficheiro.filename)
            ficheiro.save(path)

    if 'capa' in request.files:
        capa = request.files['capa']
        if capa.filename != '':
            capa.filename = request.form.get('id')
            upload_path = join(dirname(realpath(__file__)),'..' ,'elementos/static/pics/')
            capa.save(upload_path + capa.filename + '.png')

    aux = Aux
    aux.save_element(request.form['id'],request.form['titulo'],request.form['colecao'],request.form['numero'],request.form['serie'],request.form['lingua'],\
                request.form['paginas'],request.form['size'],request.form['personagens'],request.form['estado'],request.form['editora'],request.form['dataPub'],\
                request.form['tipo'],capa,path)

    return json_util.dumps({'nome': nome, 'message':'inserido com sucesso'})

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


class Aux:              
    def create_element(elem_id,titulo,numero,serie,nr_paginas,tamanho,personagens,estado,data_publicacao,capa,texto,observacoes):
        q = f'CREATE (n:Elemento\
            {{\
                id : "{elem_id}",\
                titulo : "{titulo}",\
                numero : "{numero}",\
                serie : "{serie}",\
                personagens : "{personagens}",\
                nr_paginas : "{nr_paginas}",\
                tamanho : "{tamanho}",\
                estado : "{estado}",\
                data_publicacao : "{data_publicacao}",\
                capa : "{capa}",\
                texto : "{texto}",\
                observacoes : "{observacoes}" \
            }}\
        )'
        neo4j_db.run(q)

    def create_node(nodo,designacao):
        num_id = int(neo4j_db.evaluate(f'match(n:{nodo}) return count(n)')) + 1

        if(nodo == "Autor"):
            nome = "autor_default"
            nacionalidade = "nacionalidade_default"

            neo4j_db.run(f'CREATE (n:{nodo}\
                {{\
                    id: {num_id},\
                    nome : "{nome}"\
                    nacionalidade : "{nacionalidade}"\
                }}\
            )')
        else:
            neo4j_db.run(f'CREATE (n:{nodo}\
                {{\
                    id: {num_id},\
                    designacao : "{designacao}"\
                }}\
            )')

    def create_relationship(node1,node2,first_id,second_desig,relationship):
        q = f'\
            MATCH (n1:{node1}),(n2:{node2}) \
            WHERE n1.id = "{first_id}" AND n2.designacao = "{second_desig}" \
            CREATE (n1)-[r:{relationship}]->(n2) \
            RETURN r'
        neo4j_db.run(q)
    
    def checkIfNodeExists(node,designacao):
        q = f'match(n:{node}) where n.designacao="{designacao}" return count(n)'
        return int(neo4j_db.evaluate(q)) == 1

    def save_element(elem_id,titulo,colecao,numero,serie,lingua,paginas,size,personagens,estado,editora,dataPub,tipo,capaPath,filePath):
        elem_id = elem_id
        titulo = titulo
        numero = numero
        serie = serie
        nr_paginas = paginas
        tamanho = size
        personagens = personagens
        estado = estado
        data_publicacao = dataPub
        capa = capaPath
        texto = ""
        observacoes = ""

        # ------------ New Nodes ------------
        tipo = tipo
        editora = editora
        lingua = lingua
        colecao = colecao
        # area = "Idade Média" 
        # autor = "Albert Uderzo" 
        # nacion_autor = "Francês"
        # -----------------------------------

        Aux.create_element(elem_id,titulo,numero,serie,nr_paginas,tamanho,personagens,estado,data_publicacao,capa,texto,observacoes)

        if(Aux.checkIfNodeExists("Tipo",tipo) == False):
            Aux.create_node("Tipo",tipo)
        if(Aux.checkIfNodeExists("Editora",editora) == False):
            Aux.create_node("Editora",editora)
        if(Aux.checkIfNodeExists("Lingua",lingua) == False):
            Aux.create_node("Lingua",lingua)
        if(Aux.checkIfNodeExists("Colecao",colecao) == False):
            Aux.create_node("Colecao",colecao)

        Aux.create_relationship("Elemento","Tipo",elem_id,tipo,"é")
        Aux.create_relationship("Elemento","Editora",elem_id,editora,"publicado")
        Aux.create_relationship("Elemento","Lingua",elem_id,lingua,"escrito")
        Aux.create_relationship("Elemento","Colecao",elem_id,colecao,"integra")