import pygame
from pygame.locals import *
import time

SIZE = 40

start_time = time.time()
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500,500))
        self.surface.fill((55,55,55))
        self.snake = Snake(self.surface,2)
        self.snake.draw()



    def run(self):
        running = True 

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    print('time is : ', time.time() - start_time)

                
                elif event.type == QUIT:
                    running = False

            self.snake.walk()
            time.sleep(.2) 


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()        
        self.length = length
        self.x = [SIZE]*self.length
        self.y = [SIZE]*self.length
        self.direction = 'DOWN'


    def draw(self):
        self.parent_screen.fill((110,110,5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_down(self):
        self.direction = 'DOWN'
    def move_up(self):
        self.direction = 'UP'
    def move_right(self):
        self.direction = 'RIGHT'        
    def move_left(self):
        self.direction = 'LEFT'

    def walk(self):


        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]


        if self.direction == 'UP':
            self.y -= SIZE
        if self.direction == 'DOWN':
            self.y += SIZE
        if self.direction == 'RIGHT':
            self.x += SIZE
        if self.direction == 'LEFT':
            self.x -= SIZE

        self.draw()


def draw_block(self):
    surface.fill((110,110,5))
    
    surface.blit(self.block, (self.x,self.y))
    pygame.display.flip()

if __name__ == "__main__": #wtf does this line do??? 
    game = Game()
    game.run()
    
    #initialize whole modules



    


                