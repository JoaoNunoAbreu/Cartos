from flask import jsonify, render_template, redirect, request, url_for
from app.analise import blueprint

from bson.json_util import dumps
from bson.json_util import loads 
from datetime import datetime

from flask_cors import CORS, cross_origin
CORS(blueprint)

import re
import time

@blueprint.route('/pesquisa', methods=['GET'])
def pesquisaresultados():
    palavra = request.args.get('pesquisa') 
    colecao = request.args.get('colecao') 
    editora = request.args.get('editora')
    data = request.args.get('date')
    if(data):
        datetimeobject = datetime.strptime(data,'%Y-%m-%d')
        data = datetimeobject.strftime('%d/%m/%Y')

    if colecao != "Todas" :
        if (editora != "Todas"): # col="todas" & edi="todas" 
            if (data):
                res_pesquisa = neo4j_db.run(f'match (edi:Editora)<-[:publicado]-(e:Elemento)-[:integra]->(c:Colecao) where (e.titulo contains "{palavra}" and c.designacao="{colecao}" and e.data_publicacao="{data}" and edi.designacao="{editora}") return e')
            else: 
                res_pesquisa = neo4j_db.run(f'match (edi:Editora)<-[:publicado]-(e:Elemento)-[:integra]->(c:Colecao) where (e.titulo contains "{palavra}" and c.designacao="{colecao}" and  edi.designacao="{editora}") return e')
        elif (data):
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:integra]->(c:Colecao) where (e.titulo contains "{palavra}" and c.designacao="{colecao}" and e.data_publicacao="{data}"')
        else:
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:integra]->(c:Colecao) where (e.titulo contains "{palavra}" and c.designacao="{colecao}") return e')
    elif (editora != "Todas"):
        if (data):
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:publicado]->(edi:Editora) where (e.titulo contains "{palavra}" and edi.designacao="{editora}" and e.data_publicacao="{data}") return e')
        else: 
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:publicado]->(edi:Editora) where (e.titulo contains "{palavra}" and edi.designacao="{editora}") return e')
    elif (data):
        res_pesquisa = neo4j_db.run(f'match (e:Elemento) where (e.titulo contains "{palavra}" and e.data_publicacao="{data}") return e')
    else:
        res_pesquisa = neo4j_db.run(f'match (e:Elemento) where e.titulo contains "{palavra}" return e')


    return jsonify(loads(dumps(res_pesquisa)))

# split com o operador '+'
def pesquisaIncludePalavra(palavra):

    #elimina espaços no inicio e no fim da string
    #palavra = palavra.strip()
    if not(palavra.startswith('"')) :    
        x = palavra.split()
        return x
    else : 
        return palavra

                        