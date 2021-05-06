#!/bin/bash

killall flask
export FLASK_APP=tommi.py
SUCCESS=$(flask run --host=localhost --port=16002) 
echo $SUCCESS
exit 0
