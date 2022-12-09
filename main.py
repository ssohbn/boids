from os import wait
import sys
import pygame
from random import randint
import numpy
from numpy import array, mean, ndarray, zeros

class Boid:
    def __init__(self, position: ndarray):
        self.position: ndarray = position
        self.velocity: ndarray = array([randint(-2, 2), randint(-2, 2)])

    def add_velocity(self, velocity: ndarray):
        CAP = 5

        self.velocity = self.velocity + velocity
        if self.velocity[0] > CAP:
            self.velocity[0] = CAP
        elif self.velocity[0] < -CAP:
            self.velocity[0] = -CAP

        if self.velocity[1] > CAP:
            self.velocity[1] = CAP
        elif self.velocity[1] < -CAP:
            self.velocity[1] = -CAP

    def move(self):
        self.position = self.position + self.velocity
        
def make_boids(amount: int) -> list[Boid]:
    boids = []
    for _ in range(amount):
        boids.append(Boid(array((randint(0, 500), randint(0, 500)))))

    return boids

def avg_boid_stuff(boids: list[Boid]) -> tuple[ndarray, ndarray]:
    '''
    returns tuple of avg_position and avg_velocity
    '''
    xs = []
    ys = []

    dxs = []
    dys = []

    for boid in boids:
        xs.append(boid.position[0])
        ys.append(boid.position[1])

        dxs.append(boid.velocity[0])
        dys.append(boid.velocity[1])

    x = mean(xs)
    y = mean(ys)

    dx = mean(dxs)
    dy = mean(dys)

    return array([x, y]), array([dx, dy])

def away_from_boids(boid: Boid, boids: list[Boid], distance: int):
    c = numpy.zeros(2)
    for b in boids:

        if  boid_distance(boid, b)< distance:
            c = -(b.position - boid.position) # vector away from collision

    return c

def boid_distance(a: Boid, b: Boid):
    # euclidian distance is named weird in numpy
    return numpy.linalg.norm(a.position - b.position)

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
pygame.font.init()
default_font_name = pygame.font.get_default_font()
font = pygame.font.SysFont(default_font_name, 24)

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

boids: list[Boid] = make_boids(50)

# Game loop.
while True:
    screen.fill((255,255,255))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Update.
    for boid in boids:

        close_boids = list(filter(lambda b: boid_distance(boid, b) <= 100 and b != boid, boids))
        close_birds_count = len(close_boids)

        avg_pos, avg_velocity = avg_boid_stuff(close_boids)

        to_center = (avg_pos - boid.position) / 1000
        to_avg_velocity = (avg_velocity - boid.velocity) / 10
        away = away_from_boids(boid, boids, 20) / 100

        wall_stuff = zeros(2)
        if boid.position[0] < 0:
            wall_stuff += array([0, boid.position[1]]) - boid.position
        elif boid.position[0] > width:
            wall_stuff += array([width, boid.position[1]]) - boid.position

        if boid.position[1] < 0:
            wall_stuff += array([boid.position[0], 0]) - boid.position
        elif boid.position[1] > height:
            wall_stuff += array([boid.position[0], height]) - boid.position



        if close_birds_count:
            boid.add_velocity(to_center)
            boid.add_velocity(to_avg_velocity)
        boid.add_velocity(away)
        boid.add_velocity(wall_stuff)

        next_pos = boid.position + boid.velocity * 10

        pygame.draw.line(screen, (0, 255, 0), (boid.position[0], boid.position[1]), (next_pos[0], next_pos[1]))

        boid.move()


    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))

    pygame.display.flip()
    fpsClock.tick(fps)
