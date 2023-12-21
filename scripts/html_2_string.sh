#!/bin/bash

# Function to display help
display_help() {
    echo "Usage: $0 [options] HTML_FILE"
    echo "Converts an HTML file to a single-line string."
    echo
    echo "Options:"
    echo "  -out, --output_file FILENAME  Specify the output file."
    echo "  -help, --help                 Display this help message."
    echo
    echo "Example:"
    echo "  $0 input.html"
    echo "  $0 -out output.txt input.html"
    exit 0
}

# Check if the help option is specified
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    display_help
fi

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "Please provide an HTML file as an argument."
    exit 1
fi

# Save the filename as an argument
html_file="$1"

# Check if the file exists
if [ ! -e "$html_file" ]; then
    echo "The given HTML file '$html_file' does not exist."
    exit 1
fi

# Read the HTML file, process, and create a single line string
html_string=$(awk '{gsub(/\r/,""); gsub(/"/,"\\\\\""); gsub(/'\''/,"\\\\'\''"); printf "%s", $0}' "$html_file")

# Replace line breaks (Windows -> Unix) and multiple spaces
html_string="${html_string//$'\r'/}"
html_string=$(echo "$html_string" | awk '{gsub(/  */," ")}; 1')

# Check if an output file is specified
if [ "$#" -ge 2 ]; then
    option="$2"
    file="$3"

    case $option in
    -out | --output_file)
        if [ "$file" ]; then
            output_file="$file"
            # Check if an output file already exists
            if [ -e "$output_file" ]; then
                read -p "The output file '$output_file' already exists. Do you want to overwrite it? (y/n): " answer
                if [ "$answer" != "y" ]; then
                    echo "Aborted. Exiting."
                    exit 1
                fi
            fi
            echo -e "$html_string" >"$output_file"
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
    echo "$html_string"
fi