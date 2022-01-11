import pygame
import random
import numpy as np
import time

start_time = time.time()


WIDTH = 1800
HEIGHT = 1000
BLUE = (0,0,150)
RED = (150,0,0)
BLACK = (0,0,0)

class Blob():
    def __init__(self, colour, x_boundary, y_boundary, size, start_time, life_time):
        self.colour = colour
        self.size = size
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x = random.randrange(0, self.x_boundary)
        self.y = random.randrange(0, self.y_boundary)
        self.life_time = life_time
        self.curr_time = 0
        self.gen = random.choices([False,True], cum_weights=(.3, .7), k=1)







    def move(self):
        m = 2
        self.x += random.randrange(-26*m,27*m)
        self.y += random.randrange(-26*m,27*m)

    def limits(self):
        if self.x < 0:
            self.x = 0
            # print(self.curr_time,'touched!')
        elif self.x > self.x_boundary:
            self.x = self.x_boundary
        if self.y < 0:
            self.y = 0
        elif self.y > self.y_boundary:
            self.y = self.y_boundary

    def kill(self):
        if self.curr_time >= 450:
            # self.color  = BLACK
            # print('it happened, self.curr time is ', self.curr_time)
            self.size = 0
            self.x = 1
            self.y = 1

            #kill it exit
        # if the life_time is more or equal to the time of blob the blob disappears
    def generate(self):
        if self.gen == True:
            if self.curr_time >= 150:
                pygame.draw.circle(game_display, self.colour, self.x, self.y, self.size)
        pygame.display.update()
        #generates the circle
    def regenerate(self):

        pass
        # make a copy of the cirlce 
    def convert(self):
        if self.curr_time >= 250:
            # print('conversion time')
            self.colour = BLUE

        
        # at some certain time it will turn a red cirle to blue 
    def blob_time(self, time_):
        self.curr_time += time_



pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blob world')
clock = pygame.time.Clock()


def draw_environment(blob_list):
    game_display.fill((10,10,10))
    

    for blob_id in blob_list:

        blob = blob_list[blob_id]
        # blob.generate(game_display, blob.colour, blob.x, blob.y, blob.size)
        pygame.draw.circle(game_display, blob.colour, [blob.x, blob.y], blob.size)
        blob.move()
        blob.limits()
        blob.generate()
        blob.kill()
        blob.convert()
        blob.blob_time(time.time() - start_time)

def generate(blob_list):
    pass





    pygame.display.update()

def main():
    slow_red_blobs = dict(enumerate([Blob(RED, WIDTH, HEIGHT, random.randrange(20,30), start_time, 5) for i in range(7)]))

    print("blob list is:",slow_red_blobs)
    x = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        draw_environment(slow_red_blobs) 
        clock.tick(3)        # print('actual time is', time.time() - start_time)



if __name__ == '__main__':
    main()
