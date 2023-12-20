#!/bin/bash

# GitHub Repository URL
repository_url="https://github.com/noahsbl/Learn-Python-with-Turtle-Graphics.git"

# Default target directory
default_target_directory="Learn-Python-with-Turtle-Graphics"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -dir|--directory) target_directory="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Use default target directory if not provided
target_directory="${target_directory:-$default_target_directory}" || exit 1

# Check if target directory exists
if [ -d "$target_directory" ]; then
    # If it exists, check if web_app.py is present
    if [ ! -f "$target_directory/web_app.py" ]; then
        # If web_app.py is not present, update the repository
        rm -rf "$target_directory"
        git clone "$repository_url" "$target_directory" || exit 1
    else
        # If it exists, update the repository
        cd "$target_directory" || exit 1
        git pull
        cd ..
    fi
else
    # If it doesn't exist, clone the repository
    git clone "$repository_url" "$target_directory" || exit 1
fi

# Change to the target directory
cd "$target_directory" || exit 1

# Determine the available Python version
if command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "Error: Python 3 or Python is required but not found."
    exit 1
fi

# Print the link before starting the Python HTTP server
echo "Open the following link in your browser:"
echo "http://localhost:8000/code-editor.html"

# Start Python HTTP server (default port 8000)
$python_cmd -m http.server
