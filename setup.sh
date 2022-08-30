#!/bin/bash/

sudo apt update
sudo apt install -y python3-dev
sudo apt install -y python3-venv

python3 -m venv env
source env/bin/activate
echo"Активировано виртуальное окружение"

pip instal -U pip setuptools wheel
pip install python-Levenshtein

python3 -m pip install -r requirements
