#!/bin/bash

# installation de FileManager

cd /opt/
git clone https://github.com/Cazeho/FileManager.git
cd FileManager
pip install -r rq.txt
chmod +x app.py
chmod +x reload.sh

ln -s $PWD/app.py /usr/local/bin/filemanager

filemanager
