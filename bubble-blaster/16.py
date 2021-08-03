# despite what the book says it's actually bad practice to use either:
#from tkinter import *
#from tkinter import Tk

import tkinter

HEIGHT = 500
WIDTH = 800
window =  tkinter.Tk()
window.title('Bubble Blaster')
c = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship_id = c.create_polygon(5,5,5,25,30,15,fill='red')
ship_id2 = c.create_oval(0,0,30,30,outline='red')
SHIP_RADIUS = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id,MID_X,MID_Y)
c.move(ship_id2,MID_X,MID_Y)

# don't abbreviate, it's bad style and not 'pythonic'
SHIP_SPEED = 10
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id,0,-SHIP_SPEED)
        c.move(ship_id2,0,-SHIP_SPEED)
    elif event.keysym == 'Down':
        c.move(ship_id,0,SHIP_SPEED)
        c.move(ship_id2,0,SHIP_SPEED)
    elif event.keysym == 'Left':
        c.move(ship_id,-SHIP_SPEED,0)
        c.move(ship_id2,-SHIP_SPEED,0)
    elif event.keysym == 'Right':
        c.move(ship_id,SHIP_SPEED,0)
        c.move(ship_id2,SHIP_SPEED,0)
c.bind_all('<Key>',move_ship)

import random

# adding _id to the end of a variable is not very semantic and bad practice
# each of theses bubble_ lists is easily replaced with a Bubble class
# which should always be preferred to global lists, which are considered
# major noobie fails by any professional programmer
# (see bubbles_revised.py for a better approach)
bubble_id = list()
bubble_radius = list()
bubble_speed = list()
MIN_BUBBLE_RADIUS = 10
MAX_BUBBLE_RADIUS = 30
MAX_BUBBLE_SPEED = 10
GAP = 100

def create_bubble():
    x = WIDTH + GAP
    y = random.randint(0, HEIGHT)
    r = random.randint(MIN_BUBBLE_RADIUS, MAX_BUBBLE_RADIUS)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bubble_id.append(id1)
    bubble_radius.append(r)
    bubble_speed.append(random.randint(1,MAX_BUBBLE_SPEED))

def move_bubbles():
    # the following line makes no sense based on semantics used
    # for `bubble in bubbles:` would have been so much better
    for i in range(len(bubble_id)):
        c.move(bubble_id[i], -bubble_speed[i], 0)

# the book makes an almost unnoticable note that the following should
# be 'added directly after the code you created in step 5'
# and `_num` is just redundant and bad style
def get_coords(id):
    pos = c.coords(id)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y

# this function has 'i' for the parameter while there is 'id_num' in
# others, changed to 'id' to be consistent
def del_bubble(id):
    del bubble_radius[id]
    del bubble_speed[id]
    c.delete(bubble_id[id])
    del bubble_id[id]

def clean_up_bubbles():
    for id in range(len(bubble_id)-1,-1,-1):
        x,y = get_coords(bubble_id[id])
        if x < -GAP:
            del_bubble(id)

import math
def distance(id1,id2):
    # this cal all be done more clearly with a tuple, but won't
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

# this function is out of control and needs to be seriously reworked
# it uses the idea of detecting a collision after it has happend and
# dealing with it after the fact rather than detecting it before it happens
# modified to fit into 76 columns (Python standard) but needs more
def collision():
    points = 0
    for id in range(len(bubble_id)-1,-1,-1):
        d = distance(ship_id2, bubble_id[id])
        b  = SHIP_RADIUS + bubble_radius[id]
        if d < b:
            points += bubble_radius[id] + bubble_speed[id]
            del_bubble(id)
    return points

c.create_text(50,30,text='TIME',fill='white')
c.create_text(150,30,text='SCORE',fill='white')
time_text = c.create_text(50,50,fill='white')
score_text = c.create_text(150,50,fill='white')
def show_score(score):
    c.itemconfig(score_text,text=str(score))
def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))

# the author throws in the main loop here and another import
# and constant variable that should be been grouped at the top
# plus there is no reference to the standard idiom:
# `if __name__ == '__main__':
import time
BUBBLE_CHANCE = 10
TIME_LIMIT = 30
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time.time() + TIME_LIMIT
#MAIN GAME LOOP
while time.time() < end:
    if random.randint(1, BUBBLE_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubbles()
    score += collision()
    if keyboard.press(' '):
        bubble_id.clear()
        bubble_speed.clear()
        bubble_radius.clear()
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    show_score(score)
    show_time(int(end - time.time()))
    window.update()
    time.sleep(0.01)

# use of \ for line continuations is officially discouraged
# and unnecessary

c.create_text(MID_X, MID_Y, text='GAME OVER', fill='white',
        font=('Helvetica', 30))
c.create_text(MID_X, MID_Y + 30, text='Score: ' + str(score),
        fill='white')
c.create_text(MID_X, MID_Y + 45, text='Bonus Time: ' +
        str(bonus*TIME_LIMIT), fill='white')

# added to keep the final screen up (when not using IDLE)
window.mainloop()
