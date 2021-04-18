#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'elementos_blueprint',
    __name__,
    url_prefix='/elementos',
    template_folder='templates',
    static_folder='static'
)
