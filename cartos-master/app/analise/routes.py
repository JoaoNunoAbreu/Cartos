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
    pesquisas = loadPesquisas()
    return json_util.dumps({'pesquisas': pesquisas})

@blueprint.route('/pesquisa', methods=['GET'])
def pesquisaresultados():
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

    if(data == None):
        data = "Todas"
    if(nome == "undefined"):
        nome = "Sem utilizador"
    writeSearchInFile(data_atual, nome, palavra, colecao, editora,data)

    return jsonify(loads(dumps(res_pesquisa)))

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

                        