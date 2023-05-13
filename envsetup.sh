#!/bin/sh
ls

if [ -d "env" ] 
then
    echo "Python virtual environment exists."
    rm -r env
fi

if [ -d "venv" ] 
then
    echo "Python virtual environment exists."
    rm -r venv
fi

ls

python3 -m venv venv

source venv/bin/activate

ls 
pip3 -V

pip3 install -r backend/requirements.txt

python3 backend/manage.py test

deactivate