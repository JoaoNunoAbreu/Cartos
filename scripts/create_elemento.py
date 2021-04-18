from py2neo import Graph
g = Graph("bolt://localhost:7687",password='cartos', user='neo4j') 

def create_element(elem_id,titulo,numero,serie,personagens,nr_paginas,tamanho,estado,data_publicacao,capa,texto,observacoes):
    q = f'CREATE (n:Elemento\
        {{\
            id : "{elem_id}",\
            titulo : "{titulo}",\
            numero : "{numero}",\
            serie : "{serie}",\
            personagens : {personagens},\
            nr_paginas : {nr_paginas},\
            tamanho : "{tamanho}",\
            estado : "{estado}",\
            data_publicacao : "{data_publicacao}",\
            capa : "{capa}",\
            texto : "{texto}",\
            observacoes : "{observacoes}" \
        }}\
    )'
    g.run(q)

def create_relationship(node1,node2,first_id,second_desig,relationship):
    q = f'\
        MATCH (n1:{node1}),(n2:{node2}) \
        WHERE n1.id = "{first_id}" AND n2.designacao = "{second_desig}" \
        CREATE (n1)-[r:{relationship}]->(n2) \
        RETURN r'
    g.run(q)


def main():
    num_id = int(g.evaluate(f'match(n:Elemento) return count(n)')) + 1
    elem_id = f'ELEM-{num_id}'
    titulo = "Teste"
    numero = 1
    serie = "serie1"
    nr_paginas = "50"
    tamanho = "50"
    personagens = ["Personagem1","Personagem2","Personagem3"]
    estado = "Novo"
    data_publicacao = "16/04/2021"
    capa = "path/to/file"
    texto = ""
    observacoes = ""

    # ------------ New Nodes ------------
    tipo = "T1" 
    editora = "Porto Editora" 
    lingua = "Português" 
    colecao = "C1" 
    # area = "Idade Média" 
    # autor = "Albert Uderzo" 
    # nacion_autor = "Francês"
    # -----------------------------------

    create_element(elem_id,titulo,numero,serie,nr_paginas,tamanho,personagens,estado,data_publicacao,capa,texto,observacoes)
    create_relationship("Elemento","Tipo",elem_id,tipo,"é")
    create_relationship("Elemento","Editora",elem_id,editora,"publicado")
    create_relationship("Elemento","Lingua",elem_id,lingua,"escrito")
    create_relationship("Elemento","Colecao",elem_id,colecao,"integra")

if __name__ == '__main__':
    main()