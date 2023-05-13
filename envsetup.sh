#!/bin/sh

ls
python3 -m venv venv

source venv/bin/activate

ls 
pip3 -V

pip3 install -r backend/requirements.txt

python3 backend/manage.py test

deactivate