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
from enum import Enum

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
FPS = 10

reg_mean = 5
reg_std = 3
conv_mean = 3
conv_std = .5

reg_probablity = 3
convert_prob = 5
attachment_probablity = 50

unattached_size = 5
attached_size = 20

big_step = 100
small_step = 25

#reset 
#reward
#play(action) -> direction
#game_iteration 

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    DOWN = 3


class Blob():
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

    def regenerate(self, blob_list):
        self.slow_red_blobs = blob_list
        now = time.time() - start_time
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        # cond = random.choices((True,False),weights=(reg_probablity,100-reg_probablity))[0]
        if (self.regenerate_time-.5 < self.age < self.regenerate_time+.5) and self.stuck and self.colour == RED:
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
            self.slow_red_blobs.append(new_blob)

    def convert(self, convert_prob):
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        cond = random.choices((True,False),weights=(convert_prob,100-convert_prob))[0]
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


convert_prob = .5


class Game():
    def __init__(self):

        self.game_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.convert_prob = 0.5
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.DOWN
        self.blob_size = 5
        self.slow_red_blobs = [Blob(
            RED, 
            WIDTH,
            HEIGHT,
            unattached_size, 
            time.time() - start_time, 
            random.gauss(reg_mean, reg_std),
            random.gauss(conv_mean,conv_std)) for i in range(self.blob_size)]
        self.red_blob= [redblob for redblob in self.slow_red_blobs if redblob.colour == RED and redblob.stuck]
        self.blue_blob = [blueblob for blueblob in self.slow_red_blobs if blueblob.colour == BLUE]
        
        self.score = 0
        


    def draw_text(self,text,font,text_col, x,y):
        img = font.render(text,True,text_col)
        self.game_display.blit(img,(x,y))




    def _update_ui(self):
        # global convert_prob
        self.game_display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game_display.fill((40,40,40))

        for blob in self.slow_red_blobs:

            pygame.draw.circle(self.game_display, blob.colour, [blob.body.position[0], blob.body.position[1]], blob.size)
            
            blob.move()
            blob.convert(self.convert_prob)
            blob.attach()
            blob.regenerate(self.slow_red_blobs)

        self.red_blob= [redblob for redblob in self.slow_red_blobs if redblob.colour == RED]
        self.blue_blob = [blueblob for blueblob in self.slow_red_blobs if blueblob.colour == BLUE]
        instant = time.time() - start_time
        text = 'Time Elapsed: '+str(round(instant,0)) +' second'
        self.draw_text(text,font,WHITE,20,20)
        text = 'Alive Cells: '+ str(int(len(self.red_blob))+int(len(self.blue_blob)))
        self.draw_text(text,font,WHITE,20,40)
        text = 'Differentiated Cells: '+ str(len(self.blue_blob))
        self.draw_text(text,font,WHITE,20,60)
        text = 'Chemical Dosage: '+ str(self.convert_prob)
        self.draw_text(text,font,WHITE,20,80)

        pygame.display.update()
    
    def _dose(self, direction):
        x = self.convert_prob
        if  direction == Direction.DOWN:
            x += 0
        elif direction == Direction.LEFT and self.convert_prob >=5.5:
            x -= 5
            print("got left passed")
        elif direction == Direction.RIGHT:
            x += 5
            print("got right passed")
        self.convert_prob = x




        


    def play_step(self):
        pygame.init()
        self.direction == Direction.DOWN

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print("keydown!!!!")
                if event.key == pygame.K_ESCAPE:
                    quit()  

                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                    print('left pressed')

                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                    print('right pressed')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.DOWN
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.DOWN



            if event.type == pygame.QUIT:
                print('pressed quit')
                print('current score: ', len(self.blue_blob))
                quit()  

        game_over = False

        if len(self.slow_red_blobs) > 70:
            print('Maximum blob reached ') 
            game_over = True

        if len(self.slow_red_blobs) <1:
            print('All blob died :( ')
            game_over = True
        if time.time() - start_time >= 30:
            print('time out!!!')
            
            game_over = True
        if len(self.red_blob) <= 0 and time.time() - start_time >= 10:
            print('all differentiated!!!')
            game_over = True

        self._dose(self.direction)
        self._update_ui()
        
        self.clock.tick(FPS)
        space.step(1/FPS)
        

        self.score = len(self.blue_blob)

        return game_over, self.score




    

if __name__ == '__main__':


    game = Game()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()


