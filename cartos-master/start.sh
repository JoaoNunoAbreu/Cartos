#!/bin/bash

killall flask
export FLASK_APP=cartos.py
SUCCESS=$(flask run) 
echo $SUCCESS
exit 0
