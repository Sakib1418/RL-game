from ast import Break
from cProfile import label
from cgitb import small
from curses import KEY_DOWN
from tracemalloc import start
import pygame
import random
import numpy as np
import time
from email.mime import image
from tracemalloc import start
from pygame.locals import *
import random
import numpy as np
import time
import numpy as np 
import matplotlib.pyplot as plt
import math
import pymunk

pygame.init()
font = pygame.font.SysFont('Bauhaus 93', 20)
space = pymunk.Space()
start_time = time.time()
WIDTH = 700
HEIGHT = 400
BLUE = (70,70,150)
RED = (150,70,70)
BLACK = (0,0,0)
GREY = (70,70,70)
WHITE = (255,255,255)
FPS = 5

life_mean = 30
life_std = 20
reg_mean = 5
reg_std = 2
conv_mean = 7
conv_std = 3

reg_probablity = 3
# convert_probablity = 5
attachment_probablity = 1

unattached_size = 5
attached_size = 20

big_step = 100
small_step = 10

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
game_display.fill((40,40,40))


class Blob:
    def __init__(self, colour, x_boundary, y_boundary, size, birthday, life_time, regenerate_time, convert_time):
        self.colour = colour
        self.size = size
        # self.convert_prob = 5
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.birthday = birthday
        self.life_time = life_time
        self.curr_time = time.time() - start_time
        self.age = 0
        self.regenerate_time = regenerate_time
        self.step_size = big_step
        self.stuck = False
        self.convert_time = convert_time
        self.dead = False
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, self.size+1.2)
        self.shape.elasiticy = 1
        self.shape.density = 1
        self.body.position = random.randrange(50, self.x_boundary-50),random.randrange(50, self.y_boundary-50)
        self.body.velocity = random.uniform(-self.step_size,self.step_size),random.uniform(-self.step_size,self.step_size)
        space.add(self.body,self.shape)
        # space.add(segment_shape1)

    def move(self):
        if self.stuck:
            self.step_size = small_step
        else:
            self.step_size = big_step

        move_x = random.uniform(-self.step_size,self.step_size)
        move_y = random.uniform(-self.step_size,self.step_size)
        self.body.velocity = move_x, move_y
        if self.dead:
            self.body.velocity =0,0
        else:
            pass

        if self.body.position[0] < 0+40:
            self.body.velocity = (abs(self.step_size)*3, self.body.velocity[1])
        elif self.body.position[0] > self.x_boundary-40:
            self.body.velocity = (-abs(self.step_size)*3, self.body.velocity[1])
        if self.body.position[1] < 0+40:
            self.body.velocity = (self.body.velocity[0],abs(self.step_size)*3 )
        elif self.body.position[1] > self.y_boundary-40:
            self.body.velocity= (self.body.velocity[0],-abs(self.step_size)*3)
        else:
            pass



    def kill(self):
        self.curr_time = time.time() - start_time 
        self.age = self.curr_time - self.birthday
        if self.age >= self.life_time:
            self.dead = True
            self.colour = GREY

    def regenerate(self):
        now = time.time() - start_time
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        cond = random.choices((True,False),weights=(reg_probablity,100-reg_probablity))[0]
        if (self.age > self.regenerate_time) and cond and self.stuck and self.colour == RED:
            new_blob = Blob(
                RED, 
                WIDTH,
                HEIGHT,
                attached_size, 
                now, 
                random.gauss(life_mean, life_std),
                random.gauss(reg_mean, reg_std),
                random.gauss(conv_mean, conv_std)
            )
            new_blob.body.position = self.body.position[0]+self.size,self.body.position[1]+self.size

            new_blob.stuck = True
            self.birthday =  time.time()
            slow_red_blobs.append(new_blob)

    def convert(self, convert_probability):
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        cond = random.choices((True,False),weights=(convert_probability,100-convert_probability))[0]
        if cond and self.age > self.convert_time and self.dead == False and self.colour == RED and self.stuck:
            self.colour = BLUE
            self.size = attached_size
            self.stuck = True
    
    def attach(self):
        cond = random.choices((True,False),weights=(attachment_probablity,100-attachment_probablity))[0]
        if cond and self.colour == RED:
            self.stuck = True
            self.size = attached_size
            self.step_size = small_step



   


blob_size = 10
slow_red_blobs = [Blob(
    RED, 
    WIDTH,
    HEIGHT,
    unattached_size, 
    time.time() - start_time, 
    random.gauss(life_mean, life_std),
    random.gauss(reg_mean, reg_std),
    random.gauss(conv_mean,conv_std)
) for i in range(blob_size)]   

def draw_text(game_display,text,font,text_col, x,y):
    img = font.render(text,True,text_col)
    game_display.blit(img,(x,y))




def draw_environment(blob_list, convert_probability, timex):
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    game_display.fill((40,40,40))
    # print('present convert probablity is: ,',convert_probability)
    instant = time.time() - start_time
    red_blob= [redblob for redblob in slow_red_blobs if redblob.colour == RED and redblob.stuck]
    blue_blob = [blueblob for blueblob in slow_red_blobs if blueblob.colour == BLUE]
    alive_blob = [aliveblob for aliveblob in slow_red_blobs if aliveblob.colour != GREY]
    # print('instant time is: ',instant, '; total: ',len(alive_blob),'; red blobs: ', len(red_blob), '; blue blobs: ', len(blue_blob))
    text = 'Time Elapsed: '+str(round(instant,0)) +' second'
    draw_text(game_display,text,font,WHITE,20,20)
    text = 'Alive Cells: '+ str(len(alive_blob))
    draw_text(game_display,text,font,WHITE,20,40)
    text = 'Attached Cells: '+ str(len(red_blob))
    draw_text(game_display,text,font,WHITE,20,60)
    text = 'Differentiated Cells: '+ str(len(blue_blob))
    draw_text(game_display,text,font,WHITE,20,80)
    text = 'Chemical Dosage: '+ str(convert_probability)
    draw_text(game_display,text,font,WHITE,20,100)


    for blob in blob_list:

        pygame.draw.circle(game_display, blob.colour, [blob.body.position[0], blob.body.position[1]], blob.size)
        
        blob.move()
        blob.convert(convert_probability)
        blob.attach()
        blob.regenerate()
        blob.kill()

    name = str(timex) + '.jpeg'
    pygame.image.save(game_display,name)


plt.ion()
# fig, ax = plt.subplots(figsize=(4,5))
xs, ys1, ys2, ys3 = [],[],[],[] 

def plot_enviornment(slow_red_blobs,ax):
    instant = time.time() - start_time
    red_blob= [redblob for redblob in slow_red_blobs if (redblob.colour == RED and redblob.stuck)]
    blue_blob = [blueblob for blueblob in slow_red_blobs if blueblob.colour == BLUE]
    stuck_blob = [stuckblob for stuckblob in slow_red_blobs if (stuckblob.stuck and stuckblob.colour != GREY)]
    xs.append(instant)
    ys1.append(len(red_blob))
    ys2.append(len(blue_blob))
    ys3.append(len(stuck_blob))
    
    
    plt.cla()       

    plt.plot(xs,ys1, '-r', label = 'Attached Cells')
    plt.plot(xs,ys2,'-b',label = 'Differrentiated Cells')
    plt.plot(xs,ys3,'-g', label = 'Alive Cells')
    ax.set_title(label = 'Number of Blue and Red Cells')
    ax.set_xlabel('time in seconds')
    ax.set_ylabel('# number of cells')
    ax.legend(loc = 'best')
    plt.tight_layout()
    plt.draw()
    
    plt.pause(.02)

clock = pygame.time.Clock()


class Game:
    def __init__(self):

        fig, ax = plt.subplots(figsize=(4,5))

        self.convert_probability = 0.5
        self.ax = ax
        pygame.init()

    def main(self):

        while True:
            draw_environment(slow_red_blobs,self.convert_probability, time.time()-start_time)
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    print("keydown!!!!")
                    if event.key == pygame.K_ESCAPE:
                        quit()  

                    if event.key == pygame.K_LEFT:
                        self.convert_probability += 5
                        print(self.convert_probability)
                        print('left pressed')

                    if event.key == pygame.K_RIGHT:
                        self.convert_probability -= 5
                        print(self.convert_probability)

                        print('right pressed')

                if event.type == pygame.QUIT:# or len(slow_red_blobs) <= 1 or len(slow_red_blobs) > 50:
                    print('pressed quit')
                    quit()


            # plot_enviornment(slow_red_blobs,self.ax)
            pygame.display.update()

            clock.tick(FPS)
            space.step(1/FPS)


    

if __name__ == '__main__':
    game = Game()
    game.main()
