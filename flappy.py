import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGTH = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
X = 0
Y = 1

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = [
            pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(),
            pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(),
            pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
        ]

        self.speed = SPEED

        # Currente image starts with 0 (upflap)
        self.current_image = 0

        self.image = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        # rect tupla de 4
        self.rect = self.image.get_rect()
        self.rect[0] = (SCREEN_WIDTH / 2) - self.rect[2]
        self.rect[1] = (SCREEN_HEIGTH / 2) - self.rect[3]

    def update(self):

        # Batendo asas
        # Cycle between 0 and 3
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        # Update heigt
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/pipe-green.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[X] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[Y] =  - (self.rect[3] - ysize)
        else:
            self.rect[Y] = SCREEN_HEIGTH - ysize
        
        self.mask = pygame.mask.from_surface(self.image)

        
    def update(self):
        self.rect[X] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("assets/base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect[X] = xpos
        self.rect[Y] = SCREEN_HEIGTH - GROUND_HEIGHT

    def update(self):
        # Eixo X 
        self.rect[X] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[X] < - (sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGTH - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()

# display.set_mode() create a screen game
# arguments: tuple with width and heigth
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

BACKGROUND = pygame.image.load("assets/background-day.png")
# Changing the sclae of the image 
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGTH))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(i * GROUND_WIDTH)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    

clock = pygame.time.Clock()

while True:

    clock.tick(10)
    for event in pygame.event.get():
        # Seeing whats this event
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

        
    # For each frame blit background
    screen.blit(BACKGROUND, (0,0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        
        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()
    
    pipe_group.draw(screen)
    ground_group.draw(screen)
    bird_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask)
    or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game Over
        input()
        pygame.display.update()
        break
