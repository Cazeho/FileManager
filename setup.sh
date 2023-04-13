#!/bin/bash

# installation de FileManager

cd /opt/
git clone https://github.com/Cazeho/FileManager.git
cd FileManager
chmod +x app.py

ln -s $PWD/app.py /usr/local/bin/filemanager

filemanager
