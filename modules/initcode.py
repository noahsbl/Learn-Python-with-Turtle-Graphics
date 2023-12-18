from browser import document


# button function shows initcode modal
def show_initcode_modal(ev):
    document["initcodeModal"].style.display = "block"


# function called by load_level sets initcode in modal
def set_initcode(initcode):
    if initcode != None:
        document["init_code"].text = initcode


# function sets event listeners for close initcode modal
def set_event_listeners_for_close_initcode_modal():
    initcode_modal = document["initcodeModal"]

    # set event to close button on modal to hide modal
    initcode_modal_close_button = initcode_modal.getElementsByClassName("close")[0]
    initcode_modal_close_button.bind(
        "click", lambda ev: initcode_modal.style.__setitem__("display", "none")
    )

    # set event to click in background to hide modal
    document.bind(
        "click",
        lambda event: initcode_modal.style.__setitem__("display", "none")
        if event.target == initcode_modal
        else None,
    )
