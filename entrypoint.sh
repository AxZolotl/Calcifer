#!/bin/sh

echo "Starting application..."

# Set DISPLAY to the host's display
export DISPLAY=host.docker.internal:0

echo "Using DISPLAY: $DISPLAY"

# Run the Python application
python /app/src/main.py
