# Cartos Base de Dados

Documentação oficial Neo4j para o docker container [aqui](https://neo4j.com/docs/operations-manual/current/deployment/single-instance/docker/).

Neo4j container da comunidade:

```
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/neo4j/logs:/logs \
    neo4j:latest
```

Neo4j Enterprise Edition container:

```
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --env=NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/neo4j/logs:/logs \
    neo4j:enterprise
```

Dispor as pastas `/data` e `/logs` é opcional, 
mas estas premitem navegar pelo conteúdo da base de dados, como também persistir os dados em Neo4j containers.

# Documentação

Para mais informação pode-se consultar as seguintes fontes:

* [GitHub - Docker Neo4j](https://github.com/neo4j/docker-neo4j)

* [Neo4j Docker Documentation](https://neo4j.com/docs/operations-manual/current/deployment/single-instance/docker/)

* [Docker Image  Library](https://hub.docker.com/_/neo4j/)

* [Neo4j Community](https://community.neo4j.com/)