#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# mySnakey7.py
# (c) 2015 Mal Minhas, <mal@malm.co.uk>
#
# - After School Code Club June 2015 -
# This is an implementation in Python of a simple Snake game grid
# You press <UP>,<DOWN>,<LEFT>,<RIGHT> keys to draw a green line snake.
# Important Python elements:
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
# Tkinter is Python's built-in GUI (Graphical User Interface) package.
# 4. global variables - declared at head of file.  You need to use "global"
# in a function is you are going to _change_ any global value.
# 5. spite - computer graphic which can be manipulated as a single object.
# There are sprites for food and four for different direction of
# snakey's head
# 6. resizeable window
# 7. keypress support - can now make snakey speed up and slow down by
# pressing forward or reverse!
# 8. game loop - basic loop involves: i) setting timer, ii) updating
# all object positions on timeout, iii) redrawing full scene.
#
# Good luck with Snakey!
#
# Things you could do!
# -------------------
# 1. Add monster support
# 2. Add more/different food
# 3. Add more sprites for snake

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
foodRect = None
foodSprite = 0
headSprite = 0
strawberry = None
snakeN = None
snakeE = None
snakeS = None
snakeW = None
finishedGame = False
timestep = 30
timestepfactor = 1000.0
lowerLimit = 10
upperLimit = 100


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
    if x + dx >= 0 and x + dx <= W and y + dy >= 0 and y + dy <= H:
        canvas.create_line(x, y, x + dx, y + dy,
                           width=line_width, fill=line_colour)
        x = x + dx
        y = y + dy
    else:
        if x + dx < 0:
            x = 0
        elif x + dx > W:
            x = W
        if y + dy < 0:
            y = 0
        elif y + dy > H:
            y = H


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


def updateSnake():
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
    return start, end, direction


def updateMonsters():
    pass


def pause(event):
    global finishedGame
    if not finishedGame:
        finishedGame = True
    else:
        finishedGame = False
        update_timer()


# Collision detection
def onCollision(head, seg):
    print(seg)
    start, end, direction = seg
    print(start, end)
    canvas.create_line(start[0], start[1], end[0], end[1],
                       width=line_width, fill="red")


def isCollidingWithItselfOrWall(head):
    for seg in segments:
        start, end, direction = seg
        x1, y1 = start
        x2, y2 = end
        if x1 == x2 and x1 == head[0] and head[1] >= y1 and head[1] <= y2:
            print("Colliding with itself or wall direction = %s" % direction)
            onCollision(head, seg)
            return True
        if x1 == x2 and x1 == head[0] and head[1] >= y2 and head[1] <= y1:
            print("Colliding with itself or wall direction = %s" % direction)
            onCollision(head, seg)
            return True
        if y1 == y2 and y1 == head[1] and head[0] >= x1 and head[0] <= x1:
            print("Colliding with itself or wall direction = %s" % direction)
            onCollision(head, seg)
            return True
        if y1 == y2 and y1 == head[1] and head[0] >= x2 and head[0] <= x2:
            print("Colliding with itself or wall direction = %s" % direction)
            onCollision(head, seg)
            return True
    return False


def isCollidingWithMonster(head):
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


def drawMonsters():
    pass


# Food handling
def createFood():
    ''' Generate some food within grid at random location '''
    global food
    food[0] = random.randint(foodwidth, W-foodwidth)
    food[1] = random.randint(foodwidth, H-foodwidth)


def drawFood():
    global foodSprite, foodRect
    fx, fy = food
    foodRect = canvas.create_rectangle(fx-foodwidth, fy-foodwidth,
                                       fx+foodwidth, fy+foodwidth,
                                       fill="orange")
    canvas.tag_lower(foodRect)
    # create new sprite on canvas - its center on the canvas is at (fx, fy)
    foodSprite = canvas.create_image(fx, fy, image=strawberry, anchor=CENTER)


def eatFood(startHead, endHead):
    global maxSnakeLen, foodEaten, foodRect, foodSprite
    # Delete foodRect
    canvas.delete(foodRect)
    canvas.delete(foodSprite)
    # Snake gets longer the more he eats!
    foodEaten += 1
    maxSnakeLen += 20


# Counter and timer
def drawCounters():
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


def drawSnake():
    global headSnake
    for seg in segments:
        start, end, direction = seg
        line = canvas.create_line(start[0], start[1], end[0], end[1],
                                  width=line_width, fill=line_colour)
    # Now draw head of snake which is in last segment, seg, already
    head = seg
    start, end, direction = head
    # create new sprite on canvas at (start[0], start[1])
    if direction == 'S':
        snakeImage = snakeS
    elif direction == 'N':
        snakeImage = snakeN
    elif direction == 'E':
        snakeImage = snakeE
    else:
        snakeImage = snakeW
    headSprite = canvas.create_image(start[0], start[1],
                                     image=snakeImage, anchor=CENTER)


def update_timer():
    global snakelen, segments, counter, timestep
    # Update the segment list with head, remove tail if required
    startHead, endHead, direction = updateSnake()
    updateMonsters()
    if isCollidingWithItselfOrWall(endHead):
        gameOver()
    elif isCollidingWithMonster(endHead):
        gameOver()
    elif isCollidingWithFood(endHead):
        eatFood(startHead, endHead)
        createFood()
    if startHead != endHead:
        # Now update segment list which is in reverse order - head at end
        segments.append((startHead, endHead, direction))  # to end of list
        if snakelen >= maxSnakeLen:
            segments = segments[1:]            # update list
    else:
        print("Warning startHead == endHead!")

    # length of snake is segments * length of segment
    if finishedGame:
        return
    snakelen = len(segments) * line_length
    # Redraw entire scene
    canvas.delete(ALL)
    drawSnake()
    drawFood()
    drawMonsters()
    drawCounters()
    # Reset the timer - timestep can vary from lowerLimit to upperLimit
    sliderval = timestepfactor / timestep  # timestep in ms, 50ms = 0.05s
    slider.set(sliderval)
    window.after(timestep, update_timer)


# Resize
def onResize(event):
    global W, H, finishedGame
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
window.title("MySnakey7")
canvas = Canvas(bg=bgcolour, height=H, width=W, highlightthickness=0)
strawberry = PhotoImage(file='strawberry6.gif')
snakeN = PhotoImage(file='snakeN.gif')
snakeE = PhotoImage(file='snakeE.gif')
snakeS = PhotoImage(file='snakeS.gif')
snakeW = PhotoImage(file='snakeW.gif')
resizeable = True
if resizeable:
    canvas.bind("<Configure>", onResize)
    canvas.pack(fill=BOTH, expand=1)
else:
    canvas.pack()
slider = Scale(window, length=360, width_=10, from_=lowerLimit,
               to=upperLimit, orient=HORIZONTAL, resolution=10)
sliderval = timestepfactor / timestep
slider.set(timestep)
slider.pack(fill=X)

# Bind movement to key presses
window.bind("<Up>", move_N)
window.bind("<Down>", move_S)
window.bind("<Left>", move_W)
window.bind("<Right>", move_E)
window.bind("<space>", pause)
# Execute main loop
createFood()
update_timer()
window.mainloop()
print("Final score: %d" % foodEaten)
