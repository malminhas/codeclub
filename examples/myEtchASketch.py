# My EtchASketch
# --------------
# - After School Code Club May 2014 -
# This is an implementation in Python of a simple Etch A Sketch
# You press <UP>,<DOWN>,<LEFT>,<RIGHT> keys to draw a green line.
# You press "u" to erase the window.
# There are some important new Python features in here:
# 1. Tkinter - Python's built in graphical user interface module
# 2. window - Coordinate (0,0) is in TOP LEFT HAND CORNER!
# 3. from Tkinter import * - imports all functions from Tkinter module
# 4. global variables - use 'global' in function if you are changing one
# Good luck with Etch a Sketch!
# Bonus extra: Can you think how to draw lines of different colours?
#
# Some notes on Tkinter:
# ---------------------
# - Tkinter is Python's built-in GUI (Graphical User Interface) package.
# It is a thin layer on top of a GUI framework called Tcl/Tk.  You can
# find out much more about Tkinter here: https://wiki.python.org/moin/TkInter
# - Tk is a cross-platform (Windows, Mac, Linux) graphical user interface
# toolkit designed exclusively for high-level dynamic languages like Python.
# You can find out much more about Tk here: http://www.tkdocs.com/index.html
# - Tcl is the language used to access Tk.  Tkinter is a 'wrapper' over Tcl.


import sys                      # Import Python sys module
if sys.version_info < (3, 0):   # What version of Python are we running?
    from Tkinter import *       # Tkinter module = "Tkinter" for Python 2
else:
    from tkinter import *       # and "tkinter" for Python 3!

# 1. Global variables:
canvas_height = 400             # height of window
canvas_width = 600              # width of window
canvas_colour = "black"         # background colour
p1_x = canvas_width/2           # p1_x => player 1 x direction (halfway along)
p1_y = canvas_height            # p1_y => player (at bottom of window)
p1_colour = "green"             # line colour
line_width = 5
line_length = 5


# 2. Player controls
def p1_move_up(event):
    global p1_y
    canvas.create_line(p1_x, p1_y, p1_x, (p1_y-line_length),
                       width=line_width, fill=p1_colour)
    p1_y = p1_y - line_length


def p1_move_down(event):
    global p1_y
    canvas.create_line(p1_x, p1_y, p1_x, p1_y+line_length,
                       width=line_width, fill=p1_colour)
    p1_y = p1_y + line_length


def p1_move_right(event):
    global p1_x
    canvas.create_line(p1_x, p1_y, p1_x + line_length, p1_y,
                       width=line_width, fill=p1_colour)
    p1_x = p1_x + line_length


def p1_move_left(event):
    global p1_x
    canvas.create_line(p1_x, p1_y, p1_x - line_length, p1_y,
                       width=line_width, fill=p1_colour)
    p1_x = p1_x - line_length


def erase_all(event):
    canvas.delete(ALL)


# 3. Set up window, canvas and key bindings
window = Tk()
window.title("MyEtchASketch")
canvas = Canvas(bg=canvas_colour, height=canvas_height,
                width=canvas_width, highlightthickness=0)
canvas.pack()

# 4. Bind movement to key presses
# Bind press of <UP> key to 'p1_move_up' function:
window.bind("<Up>", p1_move_up)
# Bind press of <DOWN> key to 'p1_move_down' function:
window.bind("<Down>", p1_move_down)
# Bind press of <LEFT> key to 'p1_move_left' function:
window.bind("<Left>", p1_move_left)
# Bind press of <RIGHT> key to 'p1_move_right' function:
window.bind("<Right>", p1_move_right)
# Bind press of 'u' key to 'erase_all' function:
window.bind("u", erase_all)

# 5. Execute main loop
window.mainloop()
