from browser import document, ajax, window
import json
import os

from modules import code_mirror
from modules import solution
from modules import canvas
from modules import console
from modules import initcode
from modules import theme

level_number = 0
level_index = 0
already_loaded = []
    

# function reads level parameters from json file from file system
def read_level_from_json_file(level_index):
    json_file_path = f"/levels/level_{level_index}.json"

    with open(json_file_path, "r") as json_file:
        level_parameter = json.load(json_file)

    return level_parameter


# function loads level parameters (tutorial, code, initcode, solution), clears canvas and console
def load_level():
    canvas.clear_canvas()
    console.clear_console()

    level_parameter = read_level_from_json_file(level_index)

    set_level_title(level_index)

    set_tutorial(level_parameter["tutorial"])

    if is_already_loaded(level_index):
        code_mirror.show_editor(level_index)
    elif "init_code" in level_parameter:
        code_mirror.create_code_editor(level_index, level_parameter["init_code"])
        already_loaded[level_index] = 1

    initcode.set_initcode(level_parameter["init_code"])

    solution.set_solution(level_parameter["solution_code"])

    theme.set_highlighting_theme()


# button function switches to previous level
def previous_level(ev):
    global level_index
    if level_index > 0:
        code_mirror.hide_editor(level_index)
        level_index -= 1
        load_level()


# button function switches to next level
def next_level(ev):
    global level_index
    if level_index < (level_number - 1):
        code_mirror.hide_editor(level_index)
        level_index += 1
        load_level()


# function sets level title
def set_level_title(level):
    document["level_title"].text = "Level " + str(level)


# function sets tutorial
def set_tutorial(tutorial):
    if tutorial != None:
        document["tutorial"].html = tutorial


# function sets asynchronous the number of levels on number of json file in level directory
def set_number_of_level(callback=None):
    def on_complete(req):
        global level_number
        level_files = [line.split("\"")[1] for line in req.text.splitlines() if ".json" in line]
        level_number = len(level_files)

        if callback:
            callback(level_number)

    ajax.get("/levels/", oncomplete=on_complete)


# function initializes flags in already_loaded array with zeros
def init_already_loaded(level_number):
    global already_loaded
    already_loaded = [0] * level_number


# function returns true if level is already loaded
def is_already_loaded(level):
    return already_loaded[level] == 1