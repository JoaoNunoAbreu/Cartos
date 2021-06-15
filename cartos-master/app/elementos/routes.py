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
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)
######

############################### ELEMENTOS #########################################

@blueprint.route('/elementos', methods=['GET'])
#@token_required
#@login_required
def route_template_elementos():
    """
    Get Elementos no Sistema.
    ---
    
    definitions:
      Elemento:
        type: object
        properties:
          id:
            type: integer
            description: Identificador único.
          titulo:
            type: string
            description: Titúlo.
          capa:
            type: string
            description: Capa.
          estado:
            type: string
            description: Estado do conteúdo.
          numero:
            type: integer
            description: Número
          nr_paginas:
            type: integer
            description: Número de páginas.
          texto:
            type: string
            description: Texto adicional ao Elemento.
          observacoes:
            type: string
            description: Observações textuais.
          tamanho:
            type: integer
            description: Tamanho do Elemento.
          personagens:
            type: array
            items:
              type: string
            description: Nomes das personagens do Elemento.
          serie:
            type: string
            description: Serie a que o Elemento pertence.
          data_publicacao:
            type: date
            description: Data de Publicação.
          colecao:
            type: string
            description: Coleção a que o Elemento pertence.
          editora:
            type: string
            description: Editora.
          lingua:
            type: string
            description: Língua.
          tipo:
            type: string
            description: Tipo do Elemento.

    responses:
      200:
        description: Informação do Index da Home.
        schema:
          type: array
          items:
            $ref: '#/definitions/Elemento'
    """

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
    """
    Get Elemento por ID.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Lista com o Elemento correspondente.
        schema:
          type: array
          items:
            $ref: '#/definitions/Elemento'
    """
    
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
    """
    Get Editoras.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Lista de Editoras.
        schema:
          type: array
          items:
            type: string
    """

    editoras = neo4j_db.run('match (x:Editora) return x')
    return json_util.dumps(editoras)

@blueprint.route('/colecoes', methods=['GET'])
def route_template_colecoes():
    """
    Get Coleções.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Lista de Coleções.
        schema:
          type: array
          items:
            type: string
    """
   
    colecoes = neo4j_db.run('match (x:Colecao) return x')
    return json_util.dumps(colecoes)

@blueprint.route('/linguas', methods=['GET'])
def route_template_linguas():
    """
    Get Línguas.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Lista de Línguas.
        schema:
          type: array
          items:
            type: string
    """

    linguas = neo4j_db.run('match (x:Lingua) return x')
    return json_util.dumps(linguas)

@blueprint.route('/tipos', methods=['GET'])
def route_template_tipo():
    """
    Get Tipos.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Lista de Tipos.
        schema:
          type: array
          items:
            type: string
    """

    tipos = neo4j_db.run('match (x:Tipo) return x')
    return json_util.dumps(tipos)


@blueprint.route('/ver/<elemento>/foto', methods=['GET'])
#@token_required
#@login_required
def route_template_ver_foto(elemento):
    """
    Ver foto do elemento.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Foto associada ao Elemento.
        schema:
          type: string
    """

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
def route_template_ver_video(elemento):
    """
    Ver vídeo do elemento.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Vídeo associada ao Elemento.
        schema:
          type: string
    """

    f = elemento + ".mp4"
    pathVideo = join(dirname(realpath(__file__)), 'static/pics/')
    pathCheck = join(pathVideo, f)
    if path.exists(pathCheck) :
        return send_from_directory(pathVideo, f, mimetype='video/mp4')
    else:
        return send_from_directory(pathVideo, "default", mimetype='video/png')

@blueprint.route('/ver/<elemento>/ficheiro', methods=['GET'])
def route_template_ver_ficheiro(elemento):
    """
    Ver ficheiro do elemento.
    ---
    parameters:
      - name: elemento
        in: elemento
        type: integer
        required: true

    responses:
      200:
        description: Ficheiro associada ao Elemento.
        schema:
          type: string
    """

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
def route_template_apagar(elemento):
    """
    Apagar elemento.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        
      - name: elemento
        in: elemento
        type: integer
        required: true

    definitions:
      ApagarElemento:
        type: object
        properties:
          id:
            type: string
            description: Identificador do Elemento.
          data_publicacao:
            type: string
            description: Data da publicação.
          colecao:
            type: string
            description: Coleção.
          editora:
            type: string
            description: Editora.
          lingua:
            type: string
            description: Língua.

    responses:
      200:
        description: Retorna o sucesso/insucesso da operação.
        schema:
          type: array
          items:
            $ref: '#/definitions/ApagarElemento'
    """


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
