@echo off

git pull

pip install -q -r requirements.txt

python webui.py