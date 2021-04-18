from py2neo.ogm import Model, Property, RelatedTo, RelatedFrom


class Area(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    trabalha = RelatedFrom("Area", "TRABALHA")

    pertence = RelatedFrom("Elemento", "PERTENCE")


class Autor(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    trabalha = RelatedTo(Area)

    escrito_por = RelatedFrom("Elemento", "ESCRITO_POR")


class Editora(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    preparada = RelatedFrom("Elemento", "PREPARADA")
    publicado = RelatedFrom("Colecao", "PUBLICADO")


class Colecao(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    preparada = RelatedTo(Editora)

    integra = RelatedFrom("Elemento", "INTEGRA")


class Lingua(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    idioma = RelatedFrom("Elemento", "IDIOMA")


class Tipo(Model):
    __primarykey__ = "id"

    id = Property()
    designacao = Property()

    tipadou = RelatedFrom("Elemento", "TIPADO")


class ElementoBD(Model):
    __primarykey__ = "id"

    id = Property()
    titulo = Property()
    numero = Property()
    serie = Property()
    lista_personagens = Property()
    nr_paginas = Property()
    tamanho = Property()
    estado = Property()
    data_publicacao = Property()
    capa = Property()
    texto = Property()
    observacoes = Property()

    publicado = RelatedTo(Editora)
    integra = RelatedTo(Colecao)
    idioma = RelatedTo(Lingua)
    tipado = RelatedTo(Tipo)
    escrito_por = RelatedTo(Autor)
    pertence = RelatedTo(Area)
