#!/bin/bash

# installation de FileManager

apt install python3-pip -y
pip install flask

cd /opt/
git clone https://github.com/Cazeho/FileManager.git
cd FileManager
pip install -r rq.txt
chmod +x run.sh
chmod + app.py
chmod +x reload.sh

ln -s $PWD/run.sh /usr/local/bin/filemanager

filemanager
