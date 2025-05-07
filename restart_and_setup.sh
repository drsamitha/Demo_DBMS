#!/bin/bash

# Stop the Django development server if it's running
pkill -f "python3 manage.py runserver"

# Wait a moment for the server to stop
sleep 2

# Run database setup
python3 manage.py db_setup

# Start the Django development server
python3 manage.py runserver 