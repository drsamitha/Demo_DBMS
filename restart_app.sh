#!/bin/bash

# Function to check if a process is running
is_running() {
    pgrep -f "python3 manage.py runserver" > /dev/null
}

# Stop the Django development server if it's running
if is_running; then
    echo "Stopping Django server..."
    pkill -f "python3 manage.py runserver"
    sleep 2
fi

# Run the setup process
echo "Running database setup..."
python3 manage.py run_setup

# Start the Django development server
echo "Starting Django server..."
python3 manage.py runserver 