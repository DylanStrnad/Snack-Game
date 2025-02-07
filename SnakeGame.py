# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0] # row
        j = self.pos[1] # co0lumn
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) # makes rectangle slightly smaller than grid cube
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys= pygame.key.get_pressed()

            for key in keys: # checks direction pressed, and moves. 
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns [self.head.pos[:]] = [self.dirnx, self.dirny] # snakes body only turns in spot that snakes head turns at

                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns [self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns [self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns [self.head.pos[:]] = [self.dirnx, self.dirny]

        for i , c in enumerate(self.body): # determines in pos of cube within snake is in turn location
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])   # snake will turn according to turns list
                if i == len(self.body)-1:
                    self.turns.pop(p)      # removes turn from list. prevents from turning again when crossing same location

            else: 
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])  # if at end of screen, snake will go to opposite side
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) # if snake does not meet any conditions above, it will continue moving in the same direction
                
            
    def reset(self, surface, eyes=False):

        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self): # adds cube to end of snake depending on the snakes current direction
        tail = self.body[-1]
        dx, dy = tail.dirnx , tail.dirny 

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))


 
        self.body[-1].dirnx = dx # moves the added block in the same direction as the snake body
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i ,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x=0
    y=0
    for l in range (rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0)) # makes window black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(r, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: # makws sure position is not in same place as snake. so if z is = x,y, must continue
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s) , color = (0 ,255 , 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(90) # lower means faster
        clock.tick(60) # higher means slower
        s.move()
        if s.body[0].pos == snack.pos: # if body is equal to cube pos. new cube is added to snake
            s.addCube()
            snack = cube(randomSnack(rows, s) , color = (0 ,255 , 0))

        for x in range(len(s.body)): # checks if snake collided with itself
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ' , len(s.body))
                message_box('You lost!' , 'Play again...')
                s.reset((10,10))
                break
               

        redrawWindow(win)

    pass

main()