from browser import document
import json
from collections import defaultdict

from modules import code_mirror
from modules import solution
from modules import canvas
from modules import console
from modules import initcode
from modules import theme

level_index = 0
already_loaded = defaultdict(str)


# function reads level parameters from json file from file system
def read_level_from_json_file(level_index):
    json_file_path = f"/levels/level_{level_index}.json"

    with open(json_file_path, "r") as json_file:
        level_parameter = json.load(json_file)

    return level_parameter


# function reads level parameters from python file from file system
def read_level_from_python_file(level_index):
    level_file_path = f"/levels/level_{level_index}.py"

    with open(level_file_path, "r") as level_file:
        level_code = level_file.read()

    level_parameter = {}
    exec(level_code, level_parameter)

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


# function sets level title
def set_level_title(level):
    document["level_title"].text = "Level " + str(level)


# function sets tutorial
def set_tutorial(tutorial):
    if tutorial != None:
        document["tutorial"].html = tutorial


# function returns true if level is already loaded
def is_already_loaded(level):
    return already_loaded[level] == 1


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
    if level_index < 5:
        code_mirror.hide_editor(level_index)
        level_index += 1
        load_level()
