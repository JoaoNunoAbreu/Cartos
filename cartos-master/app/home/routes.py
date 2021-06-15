#!/usr/bin/python
# -*- coding: utf-8 -*-

from calendar import leapdays
from app.home import blueprint
from flask import render_template
from flask_login import login_required
from app import token_required, neo4j_db
from app import token_required
from bson import json_util
from flask_cors import CORS, cross_origin
CORS(blueprint)

@blueprint.route('/index', methods=['GET'])
#@token_required
#@login_required
def index():
    """
    Ver Index.
    ---
    parameters:
      - name: user
        in: user
        type: string
        required: true
    
    definitions:
      IndexHome:
        type: object
        properties:
          n_users:
            type: integer
            description: Número de utilizadores.
          n_elementos:
            type: integer
            description: Número de elementos.
          n_colecoes:
            type: integer
            description: Número de coleções.
          colecoesContadas:
            type: integer
            description: Número de coleções contadas.
          editorasContadas:
            type: integer
            description: Número de editoras.
          lastElementos:
            type: array
            items:
              $ref: '#/definitions/Elemento'
            description: Array dos últimos elementos adicionados.

    responses:
      200:
        description: Informação do Index da Home.
        schema:
          $ref: '#/definitions/IndexHome'
    """

    n_users = neo4j_db.evaluate('match (x:User) return count(x)')
    n_elementos = neo4j_db.evaluate('match (x:Elemento) return count(x)')
    n_colecoes = neo4j_db.evaluate('match (x:Colecao) return count(x)')
    lastEle = neo4j_db.run('MATCH (n:Elemento) RETURN n ORDER BY n.created_at desc LIMIT 6')
    
    # --------------
    colecoes = neo4j_db.run('match (x:Colecao) return x.designacao').data()
    colecoesContadas = {}
    for i in colecoes:
        n = neo4j_db.evaluate(f"match(n:Colecao)<-[]-(b) where n.designacao=\"{i['x.designacao']}\" return count(b)")
        colecoesContadas[i['x.designacao']] = n

    # --------------
    editoras = neo4j_db.run('match (x:Editora) return x.designacao').data()
    editorasContadas = {}
    for i in editoras:
        n = neo4j_db.evaluate(f"match(n:Editora)<-[]-(b) where n.designacao=\"{i['x.designacao']}\" return count(b)")
        editorasContadas[i['x.designacao']] = n    
    

    lElem = [ ]
    for elem in lastEle :
        colecao = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Colecao) where e.id="{elem[0]["id"]}" return c.designacao')
        editora = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Editora) where e.id="{elem[0]["id"]}" return c.designacao')
        lingua = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Lingua) where e.id="{elem[0]["id"]}" return c.designacao')
        tipo = neo4j_db.evaluate(f'match (e:Elemento)-[]->(c:Tipo) where e.id="{elem[0]["id"]}" return c.designacao')
        lElem.append({
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
    data = {
        "n_users":n_users,
        "n_elementos":n_elementos,
        "n_colecoes":n_colecoes,
        "colecoesContadas":colecoesContadas,
        "editorasContadas":editorasContadas,
        "lastElementos": lElem
    }

    return json_util.dumps(data)
