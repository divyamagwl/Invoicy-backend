#!/bin/sh
if [ -d "venv" ] 
then
    rm -r venv
fi

python3 -m venv venv

source venv/bin/activate

pip3 install -r backend/requirements.txt

python3 backend/manage.py test ./backend

deactivate