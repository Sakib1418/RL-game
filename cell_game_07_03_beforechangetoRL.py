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
WHITE = (255,255,255)
FPS = 100

reg_mean = 5
reg_std = 3
conv_mean = 3
conv_std = .5

reg_probablity = 3
convert_probablity = 5
attachment_probablity = 50

unattached_size = 5
attached_size = 20

big_step = 100
small_step = 10




class Blob:
    def __init__(self, 
    colour, 
    x_boundary, 
    y_boundary, 
    size, 
    birthday,
    regenerate_time, 
    convert_time):

        self.colour = colour
        self.size = size
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.birthday = birthday
        self.curr_time = time.time() - start_time
        self.age = 0
        self.regenerate_time = regenerate_time
        self.step_size = big_step
        self.stuck = False
        self.convert_time = convert_time
        self.dead = False
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, self.size+5)
        self.shape.elasiticy = 1
        self.shape.density = 1
        self.body.position = random.randrange(250, self.x_boundary-150),random.randrange(150, self.y_boundary-100)
        self.body.velocity = random.uniform(-self.step_size,self.step_size),random.uniform(-self.step_size,self.step_size)
        space.add(self.body,self.shape)


    def move(self):
        if self.stuck:
            self.step_size = small_step
        else:
            self.step_size = big_step

        move_x = random.uniform(-self.step_size,self.step_size)
        move_y = random.uniform(-self.step_size,self.step_size)
        self.body.velocity = move_x, move_y


        if self.body.position[0] < 0+250:
            self.body.velocity = (abs(self.step_size)*3, self.body.velocity[1])
        elif self.body.position[0] > self.x_boundary-40:
            self.body.velocity = (-abs(self.step_size)*3, self.body.velocity[1])
        if self.body.position[1] < 0+150:
            self.body.velocity = (self.body.velocity[0],abs(self.step_size)*3 )
        elif self.body.position[1] > self.y_boundary-40:
            self.body.velocity= (self.body.velocity[0],-abs(self.step_size)*3)
        else:
            pass





    def regenerate(self):
        now = time.time() - start_time
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        # cond = random.choices((True,False),weights=(reg_probablity,100-reg_probablity))[0]
        if (self.regenerate_time-1 < self.age < self.regenerate_time+1) and self.stuck and self.colour == RED:
            new_blob = Blob(
                RED, 
                WIDTH,
                HEIGHT,
                attached_size, 
                now,
                random.gauss(reg_mean, reg_std),
                random.gauss(conv_mean, conv_std)
            )
            new_blob.body.position = self.body.position[0]+self.size,self.body.position[1]+self.size
            new_blob.stuck = True
            self.birthday =  time.time() - start_time
            self.regenerate_time = random.gauss(reg_mean, reg_std)
            self.convert_time = random.gauss(conv_mean, conv_std)
            slow_red_blobs.append(new_blob)

    def convert(self, convert_probability):
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        cond = random.choices((True,False),weights=(convert_probability,100-convert_probability))[0]
        if cond and self.age > self.convert_time  and self.colour == RED and self.stuck:
            self.colour = BLUE
            self.size = attached_size
            self.stuck = True
    
    def attach(self):
        cond = random.choices((True,False),weights=(attachment_probablity,100-attachment_probablity))[0]
        if cond and self.colour == RED:
            self.stuck = True
            self.size = attached_size
            self.step_size = small_step



   


blob_size = 5
slow_red_blobs = [Blob(
    RED, 
    WIDTH,
    HEIGHT,
    unattached_size, 
    time.time() - start_time, 
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
    # print('instant time is: ',instant, '; total: ',len(alive_blob),'; red blobs: ', len(red_blob), '; blue blobs: ', len(blue_blob))
    text = 'Time Elapsed: '+str(round(instant,0)) +' second'
    draw_text(game_display,text,font,WHITE,20,20)
    text = 'Alive Cells: '+ str(int(len(red_blob))+int(len(blue_blob)))
    draw_text(game_display,text,font,WHITE,20,40)
    text = 'Differentiated Cells: '+ str(len(blue_blob))
    draw_text(game_display,text,font,WHITE,20,60)
    text = 'Chemical Dosage: '+ str(convert_probability)
    draw_text(game_display,text,font,WHITE,20,80)


    for blob in blob_list:

        pygame.draw.circle(game_display, blob.colour, [blob.body.position[0], blob.body.position[1]], blob.size)
        
        blob.move()
        blob.convert(convert_probability)
        blob.attach()
        blob.regenerate()


    # name = str(timex) + '.jpeg'
    # pygame.image.save(game_display,name)


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
            blue_blob = [blueblob for blueblob in slow_red_blobs if blueblob.colour == BLUE]
            red_blob = [redblob for redblob in slow_red_blobs if redblob.colour == RED]

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

                if event.type == pygame.QUIT:
                    print('pressed quit')
                    print('current score: ', len(blue_blob))
                    quit()               
                if len(slow_red_blobs) > 70:
                    print('Maximum blob reached :O ')
                    print('current score: ', len(blue_blob))
                    quit()
                if len(slow_red_blobs) <1:
                    print('All blob died :( ')
                    quit()
                if time.time() - start_time >= 30:
                    print('time out!!!')
                    print('score is: ', len(blue_blob))
                    quit()
                if len(red_blob) <= 0:
                    print('all differentiated!!!')
                    print('score is: ', len(blue_blob))
                    quit()

            # plot_enviornment(slow_red_blobs,self.ax)
            pygame.display.update()

            clock.tick(FPS)
            space.step(1/FPS)


    

if __name__ == '__main__':
    game = Game()
    game.main()
