#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# mySnakey6.py
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
# 5. introduction of spite for food + resizeable window.  Also added support
# for making snakey speed up and slow down by pressing forward or reverse!
#
# Good luck with Snakey!
#
# Some notes on Tkinter:
# ----------------------
# - Tkinter is Python's built-in GUI (Graphical User Interface) package.
#
# Things I've learnt:
# ------------------
# 1. Python indentation is a challenge
# 2. Comments prove counter-productive in printouts
# 3. Games coding requires understanding of coordinates
# 4. Interpreter mode is useful but not for games
# 5. IDLE is confusing in duality (interpreter vs. file)
# 6. Kids want games and that means Tkinter really
# 7. Tkinter is not the easiest tool in the world
# 8. Dependencies
#
#
# TODO:
# ----
# 1. DEFINITELY: Segment handling -> canvas.delete(segment) each move.TBD
# Currently snake is never deleting any old segments + growing memory.
# 2. DEFINITELY: Add snake's head (four directions)                   TBD
# 3. DEFINITELY: Fix going in reverse                                 DONE
# 4. DEFINITELY: Fix the slider direction.  Right should be faster.   TBD
# 5. MAYBE: Add a monster
# 6. MAYBE: Add AI support

import random
try:
    from Tkinter import *
except:
    # Python3 support
    from tkinter import *

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
slider = None
counter = None
hsCounter = None
segments = []
direction = 'N'
snakelen = 0
maxSnakeLen = 100
food = [-1, -1]
foodwidth = 10
foodEaten = 0
foodSprite = 0
strawberry = None
finishedGame = False
timestep = 30
lowerLimit = 25
upperLimit = 130


def writeToFile(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def readFromFile(filename):
    with open(filename, 'r') as f:
        return f.read()

# load highest score from file
try:
    highestScore = int(readFromFile("highestScore.txt"))
    print("Loaded: %d" % highestScore)
except:
    highestScore = 0


# Player controls
def move(dx, dy):
    global x, y  # because we are updating these values
    if x + dx > 0 and x + dx < W and y + dy > 0 and y + dy < H:
        canvas.create_line(x, y, x + dx, y + dy,
                           width=line_width, fill=line_colour)
        x = x + dx
        y = y + dy


def move_N(event):
    global direction, timestep
    if direction in ['E', 'W']:
        direction = 'N'
    elif direction == 'N':
        if timestep >= lowerLimit + 5:
            timestep -= 5  # speed boost
    else:
        if timestep <= upperLimit + 5:
            timestep += 5  # speed slow


def move_E(event):
    global direction, timestep
    if direction in ['N', 'S']:
        direction = 'E'
    elif direction == 'E':
        if timestep >= lowerLimit + 5:
            timestep -= 5  # speed boost
    else:
        if timestep <= upperLimit + 5:
            timestep += 5  # speed slow


def move_S(event):
    global direction, timestep
    if direction in ['E', 'W']:
        direction = 'S'
    elif direction == 'S':
        if timestep >= lowerLimit + 5:
            timestep -= 5  # speed boost
    else:
        if timestep <= upperLimit + 5:
            timestep += 5  # speed slow


def move_W(event):
    global direction, timestep
    if direction in ['N', 'S']:
        direction = 'W'
    elif direction == 'W':
        if timestep >= lowerLimit + 5:
            timestep -= 5  # speed boost
    else:
        if timestep <= upperLimit + 5:
            timestep += 5  # speed slow


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


def pause(event):
    global finishedGame
    if not finishedGame:
        finishedGame = True
    else:
        finishedGame = False
        update_timer()


# Collision detection
def onCollision(head, seg):
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


def gameOver():
    global finishedGame
    finishedGame = True
    h = 20
    w = 100
    canvas.create_rectangle(W/2-w, H/2+h, W/2+w, H/2-h,
                            outline="red", fill=bgcolour)
    canvas.create_text(W/2, H/2, text="GAME OVER!",
                       font=("Purisa", 20), fill="red")


# Food handling
def createAndDrawFood():
    createFood()
    drawFood()


def createFood():
    ''' Generate some food within grid at random location '''
    global food, foodSprite
    food[0] = random.randint(foodwidth, W-foodwidth)
    food[1] = random.randint(foodwidth, H-foodwidth)


def drawFood():
    global foodSprite
    fx, fy = food
    rect = canvas.create_rectangle(fx-foodwidth, fy-foodwidth,
                                   fx+foodwidth, fy+foodwidth, fill="orange")
    canvas.tag_lower(rect)
    if foodSprite:  # delete old sprite
        canvas.delete(foodSprite)
        foodSprite = None
    # create new sprite on canvas - its center on the canvas is at (fx, fy)
    foodSprite = canvas.create_image(fx, fy, image=strawberry, anchor=CENTER)


def eatFood(startHead, endHead):
    global maxSnakeLen, foodEaten
    fx = food[0]
    fy = food[1]
    # Change the food colour to background colour to make it disappear
    canvas.create_rectangle(fx-foodwidth, fy-foodwidth,
                            fx+foodwidth, fy+foodwidth, fill=bgcolour)
    # Now have to ensure that any cell that is still
    # within the snake is updated to his colour
    canvas.create_line(startHead[0], startHead[1], endHead[0], endHead[1],
                       width=line_width, fill=line_colour)
    # Snake gets longer the more he eats!
    foodEaten += 1
    maxSnakeLen += 20


# Counter and timer
def updateCounters():
    global counter, hsCounter, highestScore
    if counter:
        canvas.delete(counter)
    if hsCounter:
        canvas.delete(hsCounter)
    scoreColour = "blue"
    if foodEaten >= highestScore and foodEaten > 0:
        highestScore = foodEaten
        scoreColour = "green"
        writeToFile("highestScore.txt", str(highestScore))
    canvas.create_text(35, 15, text="Score:",
                       font=("Purisa", 16), fill=scoreColour)
    offset = 65
    counter = canvas.create_text(15+offset, 15, text="%d" % foodEaten,
                                 font=("Purisa", 16), fill=scoreColour)
    canvas.create_text(W-100, 15, text="Highest Score:",
                       font=("Purisa", 16), fill="green")
    hsCounter = canvas.create_text(W-15, 15, text="%d" % highestScore,
                                   font=("Purisa", 16), fill="green")


def update_timer():
    global snakelen, segments, counter, timestep
    if finishedGame:
        return
    # Update the segment list with head, remove tail if required
    startHead, endHead = moveSnake()
    if isCollidingWithItself(endHead):
        gameOver()
    elif isCollidingWithFood(endHead):
        eatFood(startHead, endHead)
        createAndDrawFood()
    if startHead != endHead:
        segments.append((startHead, endHead))  # to end of list
        canvas.create_line(startHead[0], startHead[1], endHead[0],
                           endHead[1], width=line_width, fill=line_colour)
        if snakelen >= maxSnakeLen:
            startTail, endTail = segments[0]   # tail is first in list
            segments = segments[1:]            # update list to remove it
            canvas.create_line(startTail[0], startTail[1], endTail[0],
                               endTail[1], width=line_width, fill=bgcolour)
    # length of snake is segments * length of segment
    snakelen = len(segments) * line_length
    drawFood()
    updateCounters()
    # Reset the timer
    slider.set(timestep)  # timestep in milliseconds, 50ms = 0.05 seconds
    window.after(timestep, update_timer)


# Resize
def onResize(event):
    global W, H, finishedGame
    # Clear canvas
    canvas.delete("all")
    wscale = float(event.width)/W
    hscale = float(event.height)/H
    W = event.width
    H = event.height
    # resize the canvas
    canvas.config(width=W, height=H)
    # rescale all the objects tagged with the "all" tag
    canvas.scale("all", 0, 0, wscale, hscale)
    print("onResize: W=%d,H=%d" % (W, H))


# ################ MAIN PROGRAM ###################
# Set up window, canvas and key bindings
window = Tk()
window.title("MySnakey6")
canvas = Canvas(bg=bgcolour, height=H, width=W, highlightthickness=0)
strawberry = PhotoImage(file='strawberry6.gif')
resizeable = True
if resizeable:
    canvas.bind("<Configure>", onResize)
    canvas.pack(fill=BOTH, expand=1)
else:
    canvas.pack()
slider = Scale(window, length=360, width_=10, from_=lowerLimit,
               to=upperLimit, orient=HORIZONTAL, resolution=10)
slider.set(timestep)
slider.pack(fill=X)

# Bind movement to key presses
window.bind("<Up>", move_N)
window.bind("<Down>", move_S)
window.bind("<Left>", move_W)
window.bind("<Right>", move_E)
window.bind("<space>", pause)
# Execute main loop
createAndDrawFood()
update_timer()
window.mainloop()
print("Final score: %d" % foodEaten)
