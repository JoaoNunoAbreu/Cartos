from ogm_cartos import *

# Neo4j
from py2neo import Graph, Node
#g = Graph("http://ssh.tommi2.di.uminho.pt:7474/",password='cartosneo4j', user='neo4j')
g = Graph("bolt://localhost:7687", password='cartos', user='neo4j')
#

elem_bd = ElementoBD()

elem_bd.id = 1
elem_bd.titulo = "titulo"
elem_bd.numero = "num"
elem_bd.serie = "serie"
elem_bd.lista_personagens = ["1","2","3","2","3"]
elem_bd.nr_paginas = 1
elem_bd.tamanho = 12
elem_bd.estado = True
elem_bd.data_publicacao = "28/10/1999"
elem_bd.capa = "capa"
elem_bd.texto = "texto"
elem_bd.observacoes = "observacoes"

editora = Editora()
editora.id = 1
editora.designacao = "edit"
g.push(editora)


ling = Lingua()
ling.id = 1
ling.designacao = "ling"
g.push(ling)

tipo = Tipo()
tipo.id = 1
tipo.designacao = "tipo"
g.push(tipo)

area = Area()
area.id = 1
area.designacao = "area"
g.push(area)

colec = Colecao()
colec.id = 1
colec.designacao = "colec"
colec.preparada.add(editora)
g.push(colec)

autor = Autor()
autor.id = 1
autor.designacao = "autor"
autor.trabalha.add(area)
g.push(autor)

elem_bd.publicado.add(editora)
elem_bd.integra.add(colec)
elem_bd.idioma.add(ling)
elem_bd.tipado.add(tipo)
elem_bd.escrito_por.add(autor)
elem_bd.pertence.add(area)
g.push(elem_bd)
