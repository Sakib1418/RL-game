from ast import Break
from cProfile import label
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

random.seed(0)


start_time = time.time()
WIDTH = 700
HEIGHT = 400
BLUE = (70,70,150)
RED = (150,70,70)
BLACK = (0,0,0)
GREY = (70,70,70)
time_interval = .02

life_mean = 10
life_std = 6
reg_mean = 5
reg_std = 2
conv_mean = 7
conv_std = 3

reg_probablity = 5
convert_probablity = 10
attachment_probablity = 2

unattached_size = 5
attached_size = 15

big_step = 25
small_step = 5




class Blob:
    def __init__(self, colour, x_boundary, y_boundary, size, birthday, life_time, regenerate_time, convert_time):
        self.colour = colour
        self.size = size
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x = random.randrange(0, self.x_boundary)
        self.y = random.randrange(0, self.y_boundary)
        self.birthday = birthday
        self.life_time = life_time
        self.curr_time = time.time() - start_time
        self.age = 0
        self.regenerate_time = regenerate_time
        self.step_size = big_step
        self.stuck = False
        self.convert_time = convert_time
        self.dead = False

    def move(self):
        if self.stuck:
            self.step_size = small_step
        else:
            self.step_size = big_step

        move_x = random.randrange(-self.step_size,self.step_size)
        move_y = random.randrange(-self.step_size,self.step_size)

        if self.dead:
            move_x, move_y = 0,0
        else:
            pass

        self.x += move_x
        self.y += move_y

    def limits(self):
        if self.x < 0+40:
            self.x = 0+40
        elif self.x > self.x_boundary-40:
            self.x = self.x_boundary-40
        if self.y < 0+40:
            self.y = 0+40
        elif self.y > self.y_boundary-40:
            self.y = self.y_boundary-40



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
            new_blob.x = self.x + self.size*float(random.choices((-1,1), weights = (50,50))[0])
            new_blob.y = self.y + self.size*float(random.choices((-1,1), weights = (50,50))[0])
            new_blob.stuck = True
            slow_red_blobs.append(new_blob)

    def convert(self):
        self.curr_time = time.time() - start_time
        self.age = self.curr_time - self.birthday
        cond = random.choices((True,False),weights=(convert_probablity,100-convert_probablity))[0]
        if cond and self.age > self.convert_time and self.dead == False and self.colour == RED and self.stuck:
            self.colour = BLUE
            self.size = attached_size
            self.stuck = True
    
    def attach(self):
        # dist_list = []
        # for blob in slow_red_blobs:
        #     dist = math.sqrt(math.pow((blob.x - self.x),2) + math.pow((blob.y - self.y),2))
        #     dist_list.append(dist)

        cond = random.choices((True,False),weights=(attachment_probablity,100-attachment_probablity))[0]
        # res = True in (10 < ele < ((blob.size+self.size)+10) for ele in dist_list)
        # print(dist_list)
        if cond and self.colour == RED:
            self.stuck = True
            self.size = attached_size




size = random.randrange(10,15)        


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





def draw_environment(blob_dict,game_display):
    game_display.fill((40,40,40))
    
    instant = time.time() - start_time
    red_blob= [redblob for redblob in slow_red_blobs if redblob.colour == RED]
    blue_blob = [blueblob for blueblob in slow_red_blobs if blueblob.colour == BLUE]
    print('instant time is: ',instant, '; total: ',len(slow_red_blobs),'; red blobs: ', len(red_blob), '; blue blobs: ', len(blue_blob))


    for blob in blob_dict:

        pygame.draw.circle(game_display, blob.colour, [blob.x, blob.y], blob.size)
        blob.move()
        blob.limits()
        blob.convert()
        blob.attach()
        blob.regenerate()
        
        blob.kill()

    pygame.display.update()

plt.ion()
fig, ax = plt.subplots(figsize=(4,5))
xs, ys1, ys2, ys3 = [],[],[],[] 

def plot_enviornment(slow_red_blobs):
    instant = time.time() - start_time
    red_blob= [redblob for redblob in slow_red_blobs if redblob.colour == RED]
    blue_blob = [blueblob for blueblob in slow_red_blobs if blueblob.colour == BLUE]
    stuck_blob = [stuckblob for stuckblob in slow_red_blobs if (stuckblob.stuck and stuckblob.dead == False)]
    xs.append(instant)
    ys1.append(len(red_blob))
    ys2.append(len(blue_blob))
    ys3.append(len(stuck_blob))
    plt.cla()
    plt.plot(xs,ys1, '-r', label = 'total red blob')
    plt.plot(xs,ys2,'-b',label = 'converted blue blob')
    plt.plot(xs,ys3,'-g', label = 'stuck red blob')
    ax.set_title(label = 'Number of Blue and Red Cells')
    ax.set_xlabel('time in seconds')
    ax.set_ylabel('# number of cells')
    ax.legend(loc = 'best')
    plt.tight_layout()
    plt.draw()
    plt.pause(time_interval)


def main():
    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
        
    global slow_red_blobs 

    while True:

        draw_environment(slow_red_blobs, game_display)
        plot_enviornment(slow_red_blobs)



        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                print("keydown!!!!")
                if event.key == pygame.K_ESCAPE:
                    quit()  

                if event.key == pygame.K_LEFT:
                    print('left pressed')

                if event.key == pygame.K_RIGHT:
                    print('right pressed')

            if event.type == pygame.QUIT or len(slow_red_blobs) <= 1 or len(slow_red_blobs) > 50:
                print('pressed quit')
                quit()
        clock.tick(60)


    

if __name__ == '__main__':
    main()
