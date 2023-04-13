#!/bin/bash

# Stop the Flask server
echo "Stopping Flask server..."
pkill -f "filemanager"

echo "Start Flask server..."
filemanager
