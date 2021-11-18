#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# mySnakey4.py
# (c) 2015 Mal Minhas, <mal@malm.co.uk>
#
#
# - After School Code Club June 2015 -
# This is an implementation in Python of a simple Snake game grid
# You press <UP>,<DOWN>,<LEFT>,<RIGHT> keys to draw a green line snake.
# Important Python features in here:
# 1. Tkinter - Python's built in graphical user interface module
# 2. window - Coordinate (0,0) is the TOP LEFT CORNER!
# For a window of width W and height H, (x,y) coordinates are:
#
#       (0,0)-------------------(W,0)
#         -                       -
#         -                       -
#         -                       -
#         -                       -
#         -                       -
#         -                       -
#       (0,H)-------------------(W,H)
#
# 3. from Tkinter import * - imports all functions from Tkinter module
# 4. global variables - declared at head of file.  You need to use "global"
# in a function is you are going to _change_ any global value.
# Good luck with Snakey!
#
# Some notes on Tkinter:
# ----------------------
# - Tkinter is Python's built-in GUI (Graphical User Interface) package.
#

import sys
import time
import random
from Tkinter import *

# Global variables
H = 400
W = 600
x = W/2
y = H
line_width = 5
line_length = 5
bgcolour = "black"
line_colour = "green"
window = None
canvas = None
counter = None
segments = []
direction = 'N'
snakelen = 0
maxSnakeLen = 100
food = [-1, -1]
foodwidth = 5
foodEaten = 0
finishedGame = False


# Player controls
def move(dx, dy):
    global x, y  # because we are updating these values
    if x + dx > 0 and x + dx < W and y + dy > 0 and y + dy < H:
        canvas.create_line(x, y, x + dx, y + dy,
                           width=line_width, fill=line_colour)
        x = x + dx
        y = y + dy


def move_N(event):
    global direction
    direction = 'N'


def move_E(event):
    global direction
    direction = 'E'


def move_S(event):
    global direction
    direction = 'S'


def move_W(event):
    global direction
    direction = 'W'


def moveSnake():
    start = (x, y)
    if direction == 'N':
        move(0, -line_length)
    elif direction == 'E':
        move(line_length, 0)
    elif direction == 'S':
        move(0, line_length)
    elif direction == 'W':
        move(-line_length, 0)
    end = (x, y)   # move() updates (x,y)
    return start, end


def gameOver():
    global finishedGame
    finishedGame = True
    h = 20
    w = 100
    canvas.create_rectangle(W/2-w, H/2+h, W/2+w,
                            H/2-h, outline="red", fill=bgcolour)
    counter = canvas.create_text(W/2, H/2, text="GAME OVER!",
                                 font=("Purisa", 20), fill="red")


def createRandomFood():
    ''' Generate some food within grid at random location '''
    global food
    food[0] = random.randint(foodwidth, W-foodwidth)
    food[1] = random.randint(foodwidth, H-foodwidth)
    fx, fy = food
    canvas.create_rectangle(fx-foodwidth, fy-foodwidth,
                            fx+foodwidth, fy+foodwidth, fill="orange")


def onCollision(head, seg):
    # print("Collision!", head,seg)
    start, end = seg
    canvas.create_line(start[0], start[1], end[0], end[1],
                       width=line_width, fill="red")


def isCollidingWithItself(head):
    for seg in segments:
        x1, y1 = seg[0]
        x2, y2 = seg[1]
        if x1 == x2 and x1 == head[0] and head[1] >= y1 and head[1] <= y2:
            onCollision(head, seg)
            return True
        if x1 == x2 and x1 == head[0] and head[1] >= y2 and head[1] <= y1:
            onCollision(head, seg)
            return True
        if y1 == y2 and y1 == head[1] and head[0] >= x1 and head[0] <= x1:
            onCollision(head, seg)
            return True
        if y1 == y2 and y1 == head[1] and head[0] >= x2 and head[0] <= x2:
            onCollision(head, seg)
            return True
    return False


def isCollidingWithFood(endHead):
    sx, sy = endHead
    if sx >= (food[0]-foodwidth) and sx <= (food[0]+foodwidth):
        if (food[1]-foodwidth) <= sy <= (food[1]+foodwidth):
                return True
    return False


def eatFood(startHead, endHead):
    global maxSnakeLen, foodEaten
    fx = food[0]
    fy = food[1]
    # Change the food colour to background colour to make it disappear
    canvas.create_rectangle(fx-foodwidth, fy-foodwidth,
                            fx+foodwidth, fy+foodwidth, fill=bgcolour)
    # Now have to ensure that any cell that is still within
    # the snake is updated to his colour
    canvas.create_line(startHead[0], startHead[1], endHead[0],
                       endHead[1], width=line_width, fill=line_colour)
    # Snake gets longer the more he eats!
    foodEaten += 1
    maxSnakeLen += 20


def updateCounter():
    global counter
    if counter:
        canvas.delete(counter)
    canvas.create_rectangle(5, 5, 25, 25, outline="blue", fill=bgcolour)
    counter = canvas.create_text(15, 15, text="%d" % foodEaten,
                                 font=("Purisa", 16), fill="blue")


def update_timer():
    global snakelen, segments, counter
    if finishedGame:
        return
    # Update the segment list with head, remove tail if required
    startHead, endHead = moveSnake()
    if isCollidingWithItself(endHead):
        gameOver()
    elif isCollidingWithFood(endHead):
        eatFood(startHead, endHead)
        createRandomFood()
    if startHead != endHead:
        segments.append((startHead, endHead))  # to end of list
        canvas.create_line(startHead[0], startHead[1], endHead[0],
                           endHead[1], width=line_width, fill=line_colour)
        if snakelen >= maxSnakeLen:
            # get rid of the tail segment -> first in list
            startTail, endTail = segments[0]
            # update list to remove the tail element
            segments = segments[1:]
            canvas.create_line(startTail[0], startTail[1], endTail[0],
                               endTail[1], width=line_width, fill=bgcolour)
    # length of snake is segments * length of segment
    snakelen = len(segments) * line_length
    updateCounter()
    # Reset the timer
    timestep = 30                              # 50 milliseconds (0.05 seconds)
    window.after(timestep, update_timer)

# ############## MAIN PROGRAM ##################
# Set up window, canvas and key bindings
window = Tk()
window.title("MySnakey4")
canvas = Canvas(bg=bgcolour, height=H, width=W, highlightthickness=0)
canvas.pack()
# Bind movement to key presses
window.bind("<Up>", move_N)
window.bind("<Down>", move_S)
window.bind("<Left>", move_W)
window.bind("<Right>", move_E)
# Execute main loop
createRandomFood()
update_timer()
window.mainloop()
print("Final score: %d" % foodEaten)
