from browser import document, window
import sys
import re


# function extracts relevant part of error message
def extract_relevant_part_of_error_message(error_message):
    separator = '"<string>", '

    if separator in error_message:
        extracted_message = error_message.split(separator)[1]
        return re.sub(r'<module>', 'Code-Editor', extracted_message)
    else:
        return error_message


# function to print to console of web application
def writeConsole(*args):
    if args[0] == "\n":
        document["console"].html += "<br/>"
    else:
        extracted_part = extract_relevant_part_of_error_message("".join(args))
        document["console"].html += extracted_part


# function redirects prints and errors to console of web application
def redirect_prints_and_errors_to_console():
    sys.stdout.write = writeConsole
    sys.stderr.write = writeConsole


# function clears console
def clear_console():
    document["console"].html = ""
