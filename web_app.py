from browser import document, bind

from modules import export
from modules import solution
from modules import canvas
from modules import console
from modules import initcode
from modules import level_handler
from modules import exec_turtle
from modules import theme


# function initializes the web application
def init_webapp():
    # sets number of levels by number of json file in level directory
    # and callback initialization functions which depends on level_number
    level_handler.set_number_of_level(callback=init_objects_based_on_level_number)

    # sets font-size of buttons relative to height of button and sizes of body
    theme.set_button_size()

    # sets font-size of navbar_title and level_title relative to height of navbar and sizes of body
    theme.set_title_size()

    # sets application theme on system settings
    theme.set_application_theme_on_system_settings()

    # generates coodinates on canvas
    canvas.generate_coordinates()

    # prints and error which normaly are shown on browser buildin console are redirected to console of web application
    console.redirect_prints_and_errors_to_console()

    # sets event handler on resize events to fit canvas and coordinates to changed size
    canvas.set_resize_event_handler()

    # sets event handler for close of modal
    solution.set_event_listeners_for_close_solution_modal()
    initcode.set_event_listeners_for_close_initcode_modal()
    export.set_event_listeners_for_close_qrcode_modal()
    export.set_event_listeners_for_close_print_modal()

# callback function called by set_number_of_level calls initialization functions which depends on level_number
def init_objects_based_on_level_number(level_number):
    # initializes flags in already_loaded array with zeros
    level_handler.init_already_loaded(level_number)
    
    # loads first level (levels/level0.py) from file system
    level_handler.load_level()
    
    # initializes empty and hidden levels container for exported html content
    export.init_levels_container(level_number)
    

init_webapp()

# button bindings
document["previous_level"].bind("click", level_handler.previous_level)
document["next_level"].bind("click", level_handler.next_level)
document["export_download"].bind("click", export.export_download)
document["export_print"].bind("click", export.export_print)
document["export_qrcode"].bind("click", export.export_qrcode)
document["run_code"].bind("click", exec_turtle.run_code)
document["dark-mode-button"].bind("click", theme.toggle_application_theme)
document["show_solution"].bind("click", solution.show_solution)
document["paste_solution"].bind("click", solution.paste_solution)
document["show_solution_code"].bind("click", solution.show_solution_code)
document["show_init_code"].bind("click", initcode.show_initcode_modal)
document["toggle_coordinate_system"].bind("click", canvas.toggle_coordinate_system)
