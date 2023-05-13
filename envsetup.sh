#!/bin/sh

python3 -m venv env

ls
source env/bin/activate

pip3 install -r backend/requirements.txt