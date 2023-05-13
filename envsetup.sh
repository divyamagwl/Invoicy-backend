#!/bin/sh

python3 -m venv env

source env/bin/activate

pip3 install -r backend/requirements.txt

python3 backend/manage.py test

deactivate