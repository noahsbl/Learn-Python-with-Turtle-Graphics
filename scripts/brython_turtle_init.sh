#!/bin/bash

# Function to display help
display_help() {
    echo "Usage: $0 [options]"
    echo "Initializes the Learn-Python-with-Turtle-Graphics repository, starts the Python HTTP-server and opens webapp."
    echo
    echo "Options:"
    echo "  -dir, --directory DIRECTORY  Specify the target directory. Default is 'Learn-Python-with-Turtle-Graphics' in this directory."
    echo "  -h, --help                   Display this help message."
    echo
    exit 0
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -dir|--directory) target_directory="$2"; shift ;;
        -h|--help) display_help ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# GitHub Repository URL
repository_url="https://github.com/noahsbl/Learn-Python-with-Turtle-Graphics.git"

# Default target directory
default_target_directory="Learn-Python-with-Turtle-Graphics"

# Use default target directory if not provided
target_directory="${target_directory:-$default_target_directory}" || exit 1

# Check if target directory exists
if [ -d "$target_directory" ]; then
    # Check if target directory is empty
    if [ -z "$(ls -A "$target_directory")" ]; then
        # If it exists and is empty, update the repository
        git clone "$repository_url" "$target_directory" || exit 1
    else
        # If it exists and has content, check if web_app.py is present
        if [ ! -f "$target_directory/web_app.py" ]; then
            # If web_app.py is not present, prompt user to confirm overwriting
            read -p "Is this non-empty directory the right one and should it really be overwritten? (y/n): " answer
            if [ "$answer" != "y" ]; then
                echo "Aborted. Exiting."
                exit 1
            fi
            # Remove existing content and clone repository
            rm -rf "$target_directory"
            git clone "$repository_url" "$target_directory" || exit 1
        else
            # If it exists and has content, update the repository
            cd "$target_directory" || exit 1
            git pull || exit 1
        fi
    fi
else
    # If it doesn't exist, clone the repository
    git clone "$repository_url" "$target_directory" || exit 1
    # Change to the target directory
    cd "$target_directory" || exit 1
fi

# Determine the available Python version
if command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "Error: Python 3 or Python is required but not found."
    exit 1
fi

# Open Webapp or printing URL before starting the Python HTTP server
website_url="http://localhost:8000/code-editor.html"

# Try to open Webapp in Linux-Default-Browser
if command -v xdg-open >/dev/null; then
  xdg-open "$website_url"

# If xdg-open doesn't exist (if OS is not Linux), then try to open Webapp in macOS-Default-Browser
elif command -v open >/dev/null; then
  open "$website_url"

# If non of the commands below opens the Webapp in Default-Browser, just print URL
else
  echo "Open the following link in your browser:"
  echo "$website_url"
fi

# Start Python HTTP server (default port 8000)
$python_cmd -m http.server
