import pygame, random, math, time
 
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLACK = 0, 255, 255
WHITE = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
PURPLE = 255, 0, 255
CYAN = 0, 255, 255
 
# Classes
class Blob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = random.randint(8, 18)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(WHITE)
        self.color = BLACK
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.radius, SCREEN_WIDTH - self.radius),
                            random.randint(self.radius, SCREEN_HEIGHT - self.radius))

 
    def speed(self):
        return 50//self.radius 
 
    def move(self):
        xory = random.choice(('x', 'y'))
        x_direction = random.choice(('right', 'left'))
        y_direction = random.choice(('down', 'up'))
        if xory == 'x':
            if x_direction == 'right':
                self.rect.x += self.speed() \
                               if self.rect.right + self.speed() <= SCREEN_WIDTH \
                               else SCREEN_WIDTH - self.rect.right
            else:
                self.rect.x -= self.speed() \
                               if self.rect.left - self.speed() >= 0 \
                               else self.rect.x
        if xory == 'y':
            if y_direction == 'down':
                self.rect.y += self.speed() \
                               if self.rect.bottom + self.speed() <= SCREEN_HEIGHT \
                               else SCREEN_HEIGHT - self.rect.bottom
            else:
                self.rect.y -= self.speed() \
                               if self.rect.top - self.speed() >= 0 \
                               else self.rect.y
 
    def check_collisions(self):
        for blob in blobs:
            if pygame.sprite.collide_circle(self, blob) and blob != self:
                difference = blob.radius - self.radius
                if difference > 0:
                    blob.radius += self.radius
                    self.kill()
                elif difference < 0:
                    self.radius += blob.radius
                    blob.kill()
        if self.alive():
            self.image = pygame.Surface((self.radius * 2, self.radius * 2))
            self.image.fill(WHITE)
            temp = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = temp
 
    def update(self):
        self.check_collisions()
        self.move()
 
# Functions definitions
def add_blobs(num):
    for n in range(num):
        blobs.add(Blob())
 
def build_blobs():
    for blob in blobs:
        pygame.draw.circle(screen, blob.color, blob.rect.center, blob.radius)
     
# Essential initializations
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
 
# Other initializations
blobs = pygame.sprite.Group()
add_blobs(5)
 
running = True
# Game loop
while running:
    # Timing
    clock.tick(FPS)
 
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    # Other checks
    if len(blobs) == 1:
        running = False
 
    # Updating
    blobs.update()
 
    # Rendering
    screen.fill(WHITE)
    blobs.draw(screen)
    build_blobs()
    pygame.display.update()
 
# Quiting
pygame.quit()


