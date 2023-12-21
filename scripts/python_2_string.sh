#!/bin/bash

# Function to display help
display_help() {
    echo "Usage: $0 [options] PYTHON_FILE"
    echo "Converts a Python file to a single-line string."
    echo
    echo "Options:"
    echo "  -out, --output_file FILENAME  Specify the output file."
    echo "  -h, --help                    Display this help message."
    echo
    echo "Example:"
    echo "  $0 input.py"
    echo "  $0 -out output.txt input.py"
    exit 0
}

# Check if the help option is specified
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    display_help
fi

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "Please provide a Python file as an argument."
    exit 1
fi

# Save the filename as an argument
python_file="$1"

# Check if the file exists
if [ ! -e "$python_file" ]; then
    echo "The given Python file '$python_file' does not exist."
    exit 1
fi

# Read the Python file, process, and create a single line string
python_string=$(awk '{gsub(/\r/,""); gsub(/\t/,"\\t"); gsub(/"/,"\\\""); gsub(/'\''/,"\\'\''"); printf "%s\\n", $0}' "$python_file")

# Check if an output file is specified
if [ "$#" -ge 2 ]; then
    option="$2"
    file="$3"

    case $option in
    -out | --output_file)
        if [ "$file" ]; then
            output_file="$file"
            # Check if an output file already exist
            if [ -e "$output_file" ]; then
                read -p "The output file '$output_file' already exists. Do you want to overwrite it? (y/n): " answer
                if [ "$answer" != "y" ]; then
                    echo "Aborted. Exiting."
                    exit 1
                fi
            fi
            echo "$python_string" >"$output_file"
        else
            echo "No output file specified. Use '-out FILENAME' or '--output_file FILENAME' for specifying the output file."
            exit 1
        fi
        ;;
    *)
        echo "Undefined option: $option. Use '-out FILENAME' or '--output_file FILENAME' for specifying the output file."
        exit 1
        ;;
    esac
else
    echo "$python_string"
fi
