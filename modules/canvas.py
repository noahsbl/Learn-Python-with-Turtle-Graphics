from browser import document, window

from modules import exec_turtle
from modules import theme


# button function shows and hides coordinate system
def toggle_coordinate_system(ev):
    coordinates_element = document["coordinates"]

    if coordinates_element.style.display == "block":
        coordinates_element.style.display = "none"
    else:
        coordinates_element.style.display = "block"


# function generates coordinate system into canvas
def generate_coordinates():
    width = document["coordinates"].clientWidth
    height = document["coordinates"].clientHeight

    document["coordinates"].html = ""

    svg = (
        window.d3.select("#coordinates")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
    )

    g = svg.append("g")

    x_scale = window.d3.scaleLinear().domain([-width / 2, width / 2]).range([0, width])

    y_scale = (
        window.d3.scaleLinear().domain([-height / 2, height / 2]).range([height, 0])
    )

    x_axis = window.d3.axisBottom(x_scale)
    y_axis = window.d3.axisLeft(y_scale)

    g.append("g").attr("transform", f"translate(0, {height / 2})").call(x_axis)

    g.append("g").attr("transform", f"translate({width / 2}, 0)").call(y_axis)


# function clears canvas
def clear_canvas():
    document["canvas"].html = ""


# function is called by event listener on resize event
def resize_canvas(ev):
    theme.set_button_size()
    theme.set_title_size()
    if document.get(selector="#turtle-canvas"):
        exec_turtle.run_code(ev)
    generate_coordinates()


# sets event handler on resize event
def set_resize_event_handler():
    window.addEventListener("resize", resize_canvas)
