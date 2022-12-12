import sys
import pygame
from random import randint
import numpy
from numpy import array, ndarray, zeros

class Boid:
    def __init__(self, position: ndarray, cap):
        self.position: ndarray = position
        self.velocity: ndarray = array([randint(-2, 2), randint(-2, 2)])
        self.cap: int = cap

    def add_velocity(self, velocity: ndarray):

        self.velocity = self.velocity + velocity
        if self.velocity[0] > self.cap:
            self.velocity[0] = self.cap
        elif self.velocity[0] < -self.cap:
            self.velocity[0] = -self.cap

        if self.velocity[1] > self.cap:
            self.velocity[1] = self.cap
        elif self.velocity[1] < -self.cap:
            self.velocity[1] = -self.cap

    def move(self):
        self.position = self.position + self.velocity

def make_boids(amount: int) -> list[Boid]:
    boids = []
    for _ in range(amount):
        boids.append(Boid(array((randint(0, 500), randint(0, 500))), 50))

    return boids

def avg_boid_stuff(boids: list[Boid]) -> tuple[ndarray, ndarray]:
    '''
    returns tuple of avg_position and avg_velocity
    '''
    positions = list(map(lambda boid: boid.position, boids))
    avg_position = sum(positions) / len(positions) if len(positions) != 0 else zeros(2)

    velocities = list(map(lambda boid: boid.velocity, boids))
    avg_velocity = sum(velocities) / len(velocities) if len(velocities) != 0 else zeros(2)

    return (avg_position, avg_velocity)

def boid_distance(a: Boid, b: Boid):
    # euclidian distance is named weird in numpy
    return numpy.linalg.norm(a.position - b.position)

def away_from_boids(boid: Boid, boids: list[Boid], distance: int):
    c = numpy.zeros(2)
    for b in boids:

        #if  boid_distance(boid, b)< distance:

        diff = b.position - boid.position

        if diff[0] ** 2 + diff[1] ** 2 < distance ** 2:

            c = -(b.position - boid.position) # vector away from collision

    return c

def distance_squared(a: ndarray, b: ndarray):
    c = b-a
    d = c[0]**2 + c[1]**2
    return d

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

        close_boids = []

        for b in boids:
            if boid == b:
                continue

            diff = b.position - boid.position

            if not diff[0] ** 2 + diff[1] ** 2 < 100 ** 2:
                continue

            close_boids.append(b)

        close_boids_count = len(close_boids)

        avg_pos, avg_velocity = avg_boid_stuff(close_boids) # terrifying

        to_center = (avg_pos - boid.position) / 1000
        to_avg_velocity = (avg_velocity - boid.velocity) / 10
        away = away_from_boids(boid, boids, 20) / 100

        to_mouse = zeros(2)
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        to_mouse = (array(pygame.mouse.get_pos()) - boid.position) / 1000
        if pressed[0] and distance_squared(boid.position, array(mouse_pos)) <= 50**2:
                to_mouse *= -10

        elif not pressed[2]:
            to_mouse = (0, 0)


        wall_stuff = zeros(2)
        if boid.position[0] < 0:
            wall_stuff += array([0, boid.position[1]]) - boid.position
        elif boid.position[0] > width:
            wall_stuff += array([width, boid.position[1]]) - boid.position

        if boid.position[1] < 0:
            wall_stuff += array([boid.position[0], 0]) - boid.position
        elif boid.position[1] > height:
            wall_stuff += array([boid.position[0], height]) - boid.position

        if close_boids_count:
            boid.add_velocity(to_center)
            boid.add_velocity(to_avg_velocity)
        boid.add_velocity(to_mouse)
        boid.add_velocity(away)
        boid.add_velocity(wall_stuff)

        heading_arrow = boid.position + boid.velocity * 10

        pygame.draw.line(screen, (0, 255, 0), (boid.position[0], boid.position[1]), (heading_arrow[0], heading_arrow[1]))

        boid.move()

    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))

    text = font.render(f"fps: {fpsClock.get_fps()}", False, (0,0,0))
    screen.blit(text, (0, 0))
    
    pygame.display.flip()
    fpsClock.tick(fps)
