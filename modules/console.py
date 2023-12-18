from browser import document
import sys


# function to print to console of web application
def writeConsole(*args):
    if args[0] == "\n":
        document["console"].html += "<br/>"
    else:
        document["console"].html += "".join(args)


# function redirects prints and errors to console of web application
def redirect_prints_and_errors_to_console():
    sys.stdout.write = writeConsole
    sys.stderr.write = writeConsole


# function clears console
def clear_console():
    document["console"].html = ""
