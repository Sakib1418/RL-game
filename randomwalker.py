import pygame
import random
import numpy as np
import time

start_time = time.time()


WIDTH = 1800
HEIGHT = 1000
BLUE = (0,0,150)
RED = (150,0,0)

class Blob:
    def __init__(self, colour, x_boundary, y_boundary, size, life_time):
        self.colour = colour
        self.size = size
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x = random.randrange(0, self.x_boundary)
        self.y = random.randrange(0, self.y_boundary)
        self.life_time = life_time
        self.start_time = time.time()

    def move(self):
        self.x += random.randrange(-26,27)
        self.y += random.randrange(-26,27)

    def limits(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.x_boundary:
            self.x = self.x_boundary
        if self.y < 0:
            self.y = 0
        elif self.y > self.y_boundary:
            self.y = self.y_boundary

    def kill(self):
        pass
        # if the life_time is more or equal to the time of blob the blob disappears
    def generate(self, number_generated, x_loc, y_loc):
        pass
        #generates the circle
    def regenerate(self):
        self.color = BLUE
        pass
        # make a copy of the cirlce 
    def convert(self):
        pass
        # at some certain time it will turn a red cirle to blue 
    

    # def __add__(self, other_blob):
    #     if other_blob.size > self.size:
    #             other_blob.size += int(self.size * 0.5)
    #             self.size = 0

# class FastBlob(Blob):
#     def __init__(self, colour, x_boundary, y_boundary, size, time):
#         super().__init__(colour, x_boundary, y_boundary, size, time)
#     def move(self):
#         self.x += random.randrange(-20,21)
#         self.y += random.randrange(-20,21)

pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blob world')
clock = pygame.time.Clock()


# def is_touching(b1,b2):
#     return np.linalg.norm(np.array([b1.x,b1.y])-np.array([b2.x,b2.y])) < (b1.size + b2.size)

# def handle_collisions(blob_list):
#     blues, reds, slow_reds = blob_list
#     for first_blobs in blues, reds, slow_reds:
#         for first_blob_id, first_blob in first_blobs.copy().items():
#             for other_blobs in blues, reds, slow_reds:
#                 for other_blob_id, other_blob in other_blobs.copy().items():
#                     if first_blob == other_blob:
#                         pass
#                     else:
#                         if is_touching(first_blob, other_blob):
#                             first_blob + other_blob
#     return blues, reds, slow_reds

def draw_environment(blob_list):
    game_display.fill((10,10,10))
    # handle_collisions(blob_list)
    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(game_display, blob.colour, [blob.x, blob.y], blob.size)
            blob.move()
            blob.limits()
            # blob.kill()


    pygame.display.update()

def main():
    # blue_blobs = dict(enumerate([FastBlob(BLUE, WIDTH, HEIGHT, random.randrange(10,15), time.time() - start_time) for i in range(5)]))
    # red_blobs = dict(enumerate([FastBlob(RED, WIDTH, HEIGHT, random.randrange(5,10), time.time() - start_time) for i in range(8)]))
    slow_red_blobs = dict(enumerate([Blob(RED, WIDTH, HEIGHT, random.randrange(20,30), time.time() - start_time) for i in range(10)]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        draw_environment([slow_red_blobs])
        clock.tick(7)
        print(time.time() - start_time)

#tim = time.time() - start_time


if __name__ == '__main__':
    main()
