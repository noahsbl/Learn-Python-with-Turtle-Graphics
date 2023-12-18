from browser import document, window

from modules import level_handler

qrcode_modal = document.getElementById("qrcodeModal")
link_to_download = document.getElementById("linkToDownload")
qr_code_to_download = document.getElementById("qrCodeToDownload")
message = document.getElementById("message")
error_message = document.getElementById("errorMessage")


# button function for download export
def export_download(ev):
    create_html(download_html)


# button function for print export
def export_print(ev):
    create_html(print_html)


# button function for qrcode export
def export_qrcode(ev):
    create_html(upload_html)


# function is called onload to create container with containers for alle levels
def initialize_levels_container(level_num):
    levels_container = document["levelsContainer"]

    for level in range(level_num):
        level_container = create_container("level " + str(level))

        level_container.appendChild(create_title("H2", "Level " + str(level)))
        level_container.appendChild(create_title("H3", "Aufgabenstellung und Hinweise"))
        level_container.appendChild(
            create_container("level" + str(level) + "_exercise")
        )
        level_container.appendChild(create_title("H3", "Dein Code"))
        level_container.appendChild(create_container("level" + str(level) + "_code"))
        level_container.appendChild(create_title("H3", "Canvas"))
        level_container.appendChild(
            create_container("level" + str(level) + "_canvas_container")
        )

        if level == 0:
            level_container.classList.add("first-level-container")

        level_container.classList.add("empty-level-container")

        levels_container.appendChild(level_container)

        document["level" + str(level) + "_exercise"].html = get_exercise(level)


# function creates title
def create_title(element_type, text):
    title = document.createElement(element_type)
    title.html = text
    return title


# function creates container for an level
def create_container(container_id):
    container = document.createElement("div")
    container.id = container_id
    return container


# function reads and returns exercise from filesystem
def get_exercise(level):
    level_parameter = level_handler.read_level_from_json_file(level)
    return level_parameter["tutorial"]


# function is called by run_code to save written code and canvas to level container
def edit_level_container(level, editor):
    level_container = document["level " + str(level)]
    level_container.classList.remove("empty-level-container")

    document["level" + str(level) + "_exercise"].html = document["tutorial"].html

    add_code_from_code_mirror(document["level" + str(level) + "_code"], editor)

    canvas_container = document["level" + str(level) + "_canvas_container"]
    canvas_container.html = document["canvas"].html
    rename_animation_ids(canvas_container, level)
    set_border_on_svg(canvas_container)


# function extracts written code from code mirror object to level container
def add_code_from_code_mirror(code_container, editor):
    code_container.html = ""

    pre_element = document.createElement("pre")

    code_element = document.createElement("code")
    code_element.text = editor.getValue()

    pre_element.appendChild(code_element)
    code_container.appendChild(pre_element)

    code_container.classList.add("code-container")


# function renames ids of animation_frames to prevent conflicts on event listeners on animations in exported html file
def rename_animation_ids(canvas_container, level):
    svg = canvas_container.child_nodes[0]

    for element in svg.querySelectorAll('[id^="animation_frame"]'):
        current_id = element.id
        new_id = "level" + str(level) + "_" + current_id

        element.id = new_id

        for element in svg.querySelectorAll('[begin="' + current_id + '.end"]'):
            element.setAttribute("begin", new_id + ".end")

    svg.id = svg.id + "-" + str(level)


# function sets border on svg
def set_border_on_svg(canvas_container):
    svg = canvas_container.child_nodes[0]
    svg.style.border = "solid 1px"


# function is called by export-buttons with callback_function as parameter to export html_content
# function extracts html_content from levels container and disables hidden attribute on html_content
# gets an callback_function to export html_content
def create_html(callback_function):
    html_content = document.getElementById("levelsContainer").outerHTML
    html_content = html_content.replace('hidden=""', "")

    callback_function(html_content)


# function is an callback_function called by create_html
# creates download link and triggers it
def download_html(html_content):
    blob = window.Blob.new([html_content], {"type": "text/html"})
    url = window.URL.createObjectURL(blob)

    link = document.createElement("a")
    link.href = url
    link.download = "exported.html"

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)


# function is an callback_function called by create_html
# opens new tab with exported html_content
# modal with wait message blocks screen until animations on new tab finished and print function of browser is triggered
def print_html(html_content):
    modified_content = html_content.replace(
        "var printExport = false;", "var printExport = true;"
    )

    window.on_message_from_new_window = on_message_from_new_window
    window.addEventListener("message", on_message_from_new_window)

    new_window = window.open("", "_blank")
    new_window.document.write(modified_content)
    new_window.document.close()
    show_print_modal()


# function is called on event triggered by new print tab close
def on_message_from_new_window(event):
    if event.data == "new_window_closed":
        hide_print_modal()


# function displays print modal that blocks the web application until hide_print_modal is called
def show_print_modal():
    modal = document.getElementById("print-modal")
    modal.style.display = "block"


# function hides print modal
def hide_print_modal():
    modal = document.getElementById("print-modal")
    modal.style.display = "none"


# function is an callback_function called by create_html
# extracts html_content to a blob for post on gofile server
# fetches gofile Server and call handle_server_response for uploading html file blob
def upload_html(html_content):
    show_qr_code_modal()

    form_data = window.FormData.new()
    form_data.append(
        "file", window.Blob.new([html_content], {"type": "text/html"}), "exported.html"
    )

    window.fetch("https://api.gofile.io/getServer").then(
        lambda response: response.json()
    ).then(lambda data: handle_server_response(data, form_data)).catch(
        lambda error: handle_upload_error("Error beim Upload:\n" + error.message)
    )


# function uploads file blob on given gofile server
def handle_server_response(data, form_data):
    if data["status"] == "ok":
        upload_file_url = "https://" + data["data"]["server"] + ".gofile.io/uploadFile"
        window.fetch(upload_file_url, {"method": "POST", "body": form_data}).then(
            lambda response: response.json()
        ).then(lambda data: handle_upload_response(data)).catch(
            lambda error: handle_upload_error("Error beim Upload:\n" + error.message)
        )
    else:
        handle_upload_error("Error beim Upload:\n" + data["status"])


# function handles upload response
def handle_upload_response(data):
    if data["status"] == "ok":
        handle_upload_on_success(data)
    else:
        handle_upload_error("Error beim Upload:\n" + data["status"])


# function handles upload on success
# it shows qrcode and link to gofile download page on modal
def handle_upload_on_success(data):
    qr_code_to_download.innerHTML = ""
    qrcode = window.QRCode.new(qr_code_to_download)

    qrcode.clear()
    qrcode.makeCode(data["data"]["downloadPage"])

    link_to_download.href = data["data"]["downloadPage"]
    link_to_download.text = data["data"]["downloadPage"]

    qrcode._oDrawing._elImage.style.width = "100%"

    qr_code_to_download.style.display = "block"
    link_to_download.style.display = "block"
    message.innerText = "QR-Code scannen zum Herunterladen!"


# function handles upload on error
# it shows error message on modal
def handle_upload_error(error_msg):
    message.style.display = "none"
    error_message.innerText = error_msg
    error_message.style.display = "block"
    qrcode_modal.style.display = "block"


# function to show qrcode modal
def show_qr_code_modal():
    qr_code_to_download.style.display = "none"
    link_to_download.style.display = "none"
    error_message.style.display = "none"

    message.innerText = "Warten auf Upload ..."
    message.style.display = "block"
    qrcode_modal.style.display = "block"


# function sets event listeners for close qrcode modal
def set_event_listeners_for_close_qrcode_modal():
    # set event to close button on modal to hide modal
    qrcode_modal_close_button = qrcode_modal.getElementsByClassName("close")[0]
    qrcode_modal_close_button.bind(
        "click", lambda ev: qrcode_modal.style.__setitem__("display", "none")
    )

    # set event to click in background to hide modal
    document.bind(
        "click",
        lambda event: qrcode_modal.style.__setitem__("display", "none")
        if event.target == qrcode_modal
        else None,
    )

# function sets event listeners for close print modal
def set_event_listeners_for_close_print_modal():
    print_modal = document.getElementById("print-modal")
    # set event to close button on modal to hide modal
    print_modal_close_button = print_modal.getElementsByClassName("close")[0]
    print_modal_close_button.bind(
        "click", lambda ev: print_modal.style.__setitem__("display", "none")
    )

    # set event to click in background to hide modal
    document.bind(
        "click",
        lambda event: print_modal.style.__setitem__("display", "none")
        if event.target == print_modal
        else None,
    )