# tommi

Respositório do Tommi - Partilha com os grupos do LEI.

Run Tommi:

Para correr tommi em localhost, fazer:

If first time:

- install python
- install pip
- pip install -r requirements.txt
- Start Mongo
- export FLASK_APP=tommi.py ; flask run

else:

- Start Mongo
- export FLASK_APP=tommi.py ; flask run

## Erros

Se der erro:

- JWT: 'module' object has no attribute 'encode'
  - pip uninstall JWT
  - pip uninstall PyJWT
  - pip install PyJWT
