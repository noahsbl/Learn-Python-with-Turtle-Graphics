from browser import document, window

from modules import code_mirror


# button function toggles theme of web application
def toggle_application_theme(ev):
    document.body.classList.toggle("darkmode")

    document["qrcode-modal-content"].classList.toggle("darkmode")
    document["initcode-modal-content"].classList.toggle("darkmode")
    document["solution-modal-content"].classList.toggle("darkmode")
    document["print-modal-content"].classList.toggle("darkmode")

    document["linkToDownload"].classList.toggle("darkmode")

    document["solution_password"].classList.toggle("darkmode")

    buttons = document.select("button")
    for button in buttons:
        button.classList.toggle("darkmode")

    if document["dark-mode-button"].text == "Dark Mode":
        document["dark-mode-button"].text = "Light Mode"
    else:
        document["dark-mode-button"].text = "Dark Mode"

    set_navbar_image()
    set_highlighting_theme()


# function sets theme of code editor of current level
def set_highlighting_theme():
    if document["dark-mode-button"].text == "Dark Mode":
        code_mirror.set_theme("vscode-light")
    else:
        code_mirror.set_theme("vscode-dark")


# function sets application theme on system settings
def set_application_theme_on_system_settings():
    dark = window.matchMedia("(prefers-color-scheme:dark)").matches
    if dark:
        toggle_application_theme(None)


# function sets navbar image on theme change
def set_navbar_image():
    navbar_image = document["navbar-image"]

    if document["dark-mode-button"].text == "Dark Mode":
        navbar_image.src = "images/turtle_lightmode.png"
    else:
        navbar_image.src = "images/turtle_darkmode.png"


# function sets font-size of buttons relative to height of button and sizes of body
def set_button_size():
    buttons = document.select("button")
    for button in buttons:
        body_width = document.body.clientWidth
        body_height = document.body.clientHeight
        button_height = button.clientHeight

        if is_dropdown_button(button) or is_button_in_modal(button) or is_darkmode_button(button):
            button_height = document["run_code"].clientHeight

        factor = 0.32
        font_size = factor * (body_width / body_height) * button_height

        button.style.fontSize = str(font_size) + "px"


# function returns True if given button is a dropdown button
def is_dropdown_button(button):
    return "dropdown-button" in button.getAttribute("class").split()


# function returns True if given button is a button in modal
def is_button_in_modal(button):
    return button.id == "show_solution_code" or button.id == "paste_solution"


def is_darkmode_button(button):
    return button.id == "dark-mode-button"


# function sets font-size of navbar_title and level_title relative to height of navbar and sizes of body
def set_title_size():
    navbar_container = document["navbar_container"]
    navbar_title = document["navbar_title"]
    level_title = document["level_title"]

    body_width = document.body.clientWidth
    body_height = document.body.clientHeight
    navbar_container_height = navbar_container.clientHeight

    factor = 0.21

    font_size = factor * (body_width / body_height) * navbar_container_height

    navbar_title.style.fontSize = str(font_size) + "px"
    level_title.style.fontSize = str(font_size) + "px"
