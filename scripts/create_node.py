from py2neo import Graph
g = Graph("bolt://localhost:7687",password='cartos', user='neo4j') 

print("Nodo: ",end="")
nodo = input()

num_id = int(g.evaluate(f'match(n:{nodo}) return count(n)')) + 1

if(nodo != "Autor"):

    print("Designação: ",end="")
    designacao = input()

    g.run(f'CREATE (n:{nodo}\
        {{\
            id: {num_id},\
            designacao : "{designacao}"\
        }}\
    )')
else:
    print("Nome: ",end="")
    nome = input()

    print("Nacionalidade: ",end="")
    nacionalidade = input()

    g.run(f'CREATE (n:{nodo}\
        {{\
            id: {num_id},\
            nome : "{nome}"\
            nacionalidade : "{nacionalidade}"\
        }}\
    )')