from browser import document
import re

from modules import code_mirror


# button function for show solution modal with comment solution
def show_solution(ev):
    document["solution_comments_container"].style.display = "block"
    document["solution_code_container"].style.display = "none"
    document["solutionModal"].style.display = "block"


# button function for insert code solution to code editor
def paste_solution(ev):
    code_mirror.setCodeMirrorContent(document["solution_code"].text)


# button function for check password and show code solution
def show_solution_code(ev):
    if document["solution_password"].value == "Passwort":
        document["solution_comments_container"].style.display = "none"
        document["solution_code_container"].style.display = "block"
        document["solution_password"].value = ""
    else:
        document["solution_password"].value = ""


# function called by load_level to set solution for modal
def set_solution(solution):
    document["solution_code"].text = solution
    document["solution_comments"].text = get_solution_comments(solution)


# function extracts comments from given code
def get_solution_comments(code):
    lines = code.split("\n")
    comment_lines = []

    for line in lines:
        if "#" in line:
            tabs = ""
            num_of_tabs = code_mirror.count_tabs_in_line(line)
            for i in range(num_of_tabs):
                tabs += "\t"
            comment_lines.append(tabs + re.sub(re.compile(r"(.*)#"), r"#", line))
        else:
            comment_lines.append("")

    return "\n".join(comment_lines)


# function sets event listeners for close solution modal
def set_event_listeners_for_close_solution_modal():
    soultion_modal = document["solutionModal"]

    # set event to close button on modal to hide modal
    soultion_modal_close_button = soultion_modal.getElementsByClassName("close")[0]
    soultion_modal_close_button.bind(
        "click", lambda ev: soultion_modal.style.__setitem__("display", "none")
    )

    # set event to click in background to hide modal
    document.bind(
        "click",
        lambda event: soultion_modal.style.__setitem__("display", "none")
        if event.target == soultion_modal
        else None,
    )
