from py2neo import Graph, NodeMatcher
g = Graph("bolt://localhost:7687",password='cartos', user='neo4j') 
result = g.run('Match (x:Elemento) return x')

for i in result:
    print(i[0]['id'])
    result2 = g.run('match (e:Elemento)-[]->(c:Colecao) where e.id="ELEM-5" return c.designacao')
    for j in result2:
        print("j = {j[0]['id']}")
