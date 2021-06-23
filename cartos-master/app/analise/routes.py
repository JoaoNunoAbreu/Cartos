from flask import jsonify, render_template, redirect, request, url_for
from app.analise import blueprint
from app import neo4j_db
from bson.json_util import dumps
from bson.json_util import loads 
from datetime import datetime
from app import token_required, admin_required, photo_auth, neo4j_db


from flask_cors import CORS, cross_origin
CORS(blueprint)
import json
from bson import json_util


############################### PESQUISAS FEITAS #########################################

@blueprint.route('/pesquisas', methods=['GET'])
@token_required
def route_pesquisas():
    """
    Consultar pesquisas anteriormente efetuadas.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

    definitions:
      PesquisasObj:
        type: object
        properties:
          message:
            type: string
            description: Resultado do Logout.

    responses:
      200:
        description: Pesquisas Realizadas.
        schema:
          $ref: '#/definitions/PesquisasObj'
    """

    pesquisas = loadPesquisas()
    return json_util.dumps({'pesquisas': pesquisas})

@blueprint.route('/pesquisa', methods=['GET'])
def pesquisaresultados():
    """
    Efetuar uma nova pesquisa.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true

      - in: query
        name: pesquisa
        type: string
        required: true

      - in: query
        name: colecao
        type: string
        required: true

      - in: query
        name: editora
        type: string
        required: true

      - in: query
        name: date
        type: string
        required: false

      - in: query
        name: nome
        type: string
        required: true


    definitions:
      PesquisaObj:
        type: object
        properties:
          message:
            type: string
            description: Resultado da Pesquisa.

    responses:
      200:
        description: Resultado da Pesquisa.
        schema:
          $ref: '#/definitions/PesquisaObj'
    """

    palavra = request.args.get('pesquisa') 
    colecao = request.args.get('colecao') 
    editora = request.args.get('editora')
    data = request.args.get('date')
    nome = request.args.get('nome')

    now = datetime.now()
    data_atual = now.strftime("%Y-%m-%d %H:%M:%S.%f")

    if(data):
        datetimeobject = datetime.strptime(data,'%Y-%m-%d')
        data = datetimeobject.strftime('%d/%m/%Y')

    if colecao != "Todas" :
        if (editora != "Todas"): # col="todas" & edi="todas" 
            if (data):
                res_pesquisa = neo4j_db.run(f'match (edi:Editora)<-[:publicado]-(e:Elemento)-[:integra]->(c:Colecao) where (toLower(e.titulo) contains toLower("{palavra}") and c.designacao="{colecao}" and e.data_publicacao="{data}" and edi.designacao="{editora}") return e')
            else: 
                res_pesquisa = neo4j_db.run(f'match (edi:Editora)<-[:publicado]-(e:Elemento)-[:integra]->(c:Colecao) where (toLower(e.titulo) contains toLower("{palavra}") and c.designacao="{colecao}" and  edi.designacao="{editora}") return e')
        elif (data):
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:integra]->(c:Colecao) where (toLower(e.titulo) contains toLower("{palavra}") and c.designacao="{colecao}" and e.data_publicacao="{data}") return e')
        else:
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:integra]->(c:Colecao) where (toLower(e.titulo) contains toLower("{palavra}") and c.designacao="{colecao}") return e')
    elif (editora != "Todas"):
        if (data):
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:publicado]->(edi:Editora) where (toLower(e.titulo) contains toLower("{palavra}") and edi.designacao="{editora}" and e.data_publicacao="{data}") return e')
        else: 
            res_pesquisa = neo4j_db.run(f'match (e:Elemento)-[:publicado]->(edi:Editora) where (toLower(e.titulo) contains toLower("{palavra}") and edi.designacao="{editora}") return e')
    elif (data):
        res_pesquisa = neo4j_db.run(f'match (e:Elemento) where (toLower(e.titulo) contains toLower("{palavra}") and e.data_publicacao="{data}") return e')
    else:
        res_pesquisa = neo4j_db.run(f'match (e:Elemento) where toLower(e.titulo) contains toLower("{palavra}") return e')

    if(data == None):
        data = "Todas"
    if(nome == "undefined"):
        nome = "Sem utilizador"
    writeSearchInFile(data_atual, nome, palavra, colecao, editora,data)

    ''' Buscar resto de informação '''

    data = [ ]
    for elem in res_pesquisa:
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

def loadPesquisas():
    with open('pesquisas.json') as json_file:
        pesquisas = json.load(json_file)
    return pesquisas

def writeSearchInFile(data_atual, nome, palavra, colecao, editora,data):
    p = {"data_atual": str(data_atual), "nome":nome, "palavra":palavra, "colecao":colecao,"editora":editora, "data":data}

    pesquisas = loadPesquisas()

    pesquisas.append(p)

    with open('pesquisas.json', 'w') as outfile:
        json.dump(pesquisas, outfile,indent=4,ensure_ascii=False)


# split com o operador '+'
def pesquisaIncludePalavra(palavra):

    #elimina espaços no inicio e no fim da string
    #palavra = palavra.strip()
    if not(palavra.startswith('"')) :    
        x = palavra.split()
        return x
    else : 
        return palavra

                        