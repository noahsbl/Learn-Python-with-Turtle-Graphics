from browser import document, window, bind
import turtle

from modules import code_mirror
from modules import export
from modules import console
from modules import level_handler


# button function runs code from code editor
def run_code(ev):
    console.clear_console()

    code = code_mirror.getCodeMirrorContent(level_handler.level_index)
    code_with_turtle_rollback = code + "\n\nturtle.done()"

    turtle.restart()
    exec(code_with_turtle_rollback)

    export.edit_level_container(
        level_handler.level_index, code_mirror.editors[level_handler.level_index]
    )


# function is called by user code in code editor
# it initializes turtle for usage
# user can't delete the call in code editor
def init_turtle(turtle):
    turtle.set_defaults(
        canvwidth=document["canvas"].clientWidth,
        canvheight=document["canvas"].clientHeight,
    )
    t = turtle.Turtle()
    t.width(5)
    return t


# function teleports to given position
def teleport(t, x=0, y=0):
    was_visible = t.isvisible()
    t.hideturtle()
    t.penup()
    old_speed = t.speed()
    t.speed(10)
    
    t.goto(x, y)

    t.speed(old_speed)
    t.pendown()
    if was_visible:
        t.showturtle()
