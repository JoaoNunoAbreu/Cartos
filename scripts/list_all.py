from py2neo import Graph
g = Graph("bolt://localhost:7687",password='cartos', user='neo4j') 
result = g.run('MATCH(n) return n')

for i in result:
    print(i)
