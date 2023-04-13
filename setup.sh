#!/bin/bash

# installation de FileManager

cd /opt/
git clone https://github.com/Cazeho/FileManager.git
cd FileManager
pip install -r rq.txt
chmod +x run.sh
chmod + app.py
chmod +x reload.sh

ln -s $PWD/run.sh /usr/local/bin/filemanager

filemanager
