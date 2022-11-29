# rules of boids
# separation: steer to avoid crowding local flockmates
# alignment: steer towards the average heading of local flockmates
# cohesion: steer to move towards the average position (center of mass) of local flockmates
import sys
import pygame
from math import radians, degrees, sin, cos, atan, sqrt
from random import randint
from numpy import mean

class Boid:
    def __init__(self, direction: int, position: tuple[int, int], speed: int):
        self.direction: int = direction
        self.position: tuple[int, int] = position
        self.speed: int = speed

    def rotate(self, direction: int):
        dd = direction - self.direction 

        negative = False
        if dd < 0:
            negative = True

        if abs(dd) > 30: # clamp it? maybe smoother boid?
            dd = 30

        if negative:
            dd *= -1

        self.direction += dd


    def move(self):
        x,y = self.position
        direction = radians(self.direction)
        x = x + (cos(direction) * self.speed)
        y = y - (sin(direction) * self.speed) # - moves down
        self.position = (int(x), int(y)) # this cast may be very annoying in the future

def make_some_boids(amount: int, grid_dimensions: tuple[int, int], speed: int) -> list[Boid]:
    boids = []
    for _ in range(amount):
        boids.append(Boid(randint(-180, 180), (randint(0, grid_dimensions[0]), randint(0, grid_dimensions[1])), speed))

    return boids

def average_boid_stuff(boids: list[Boid]) -> tuple[int, tuple[int, int]]:
    rotations = []
    xs = []
    ys = []
    for boid in boids:
        rotations.append(boid.direction)
        xs.append(boid.position[0])
        ys.append(boid.position[1])

    return int(mean(rotations)), (int(mean(xs)), int(mean(ys)))


pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

boids = make_some_boids(100, (width, height), 10)
 

def pt_to_pt_angle_deg(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay

    #  1|0
    #-------
    #  2|3
    
    if dx >= 0 and dy <= 0:
        q = 0
    elif dx <= 0 and dy <= 0:
        q = 1
    elif dx <= 0 and dy >= 0:
        q = 2
    else:
        q = 3

    try:
        #return int(abs(degrees(atan(dy/dx)))) #+ (90 * q)

        match q:
            case 0:
                return int(abs(degrees(atan(dy/dx)))) + (90 * q)
            case 1:
                return 90-int(abs(degrees(atan(dy/dx)))) + (90 * q)
            case 2:
                return int(abs(degrees(atan(dy/dx)))) + (90 * q)
            case 3:
                return 90-int(abs(degrees(atan(dy/dx)))) + (90 * q)

    except ZeroDivisionError:
        return 0

def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay
    return int(sqrt(dx ** 2 + dy ** 2))

# Game loop.
while True:
    screen.fill((255,255,255))
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    for boid in boids:
        boid.move()

        avg_rotation, avg_position = average_boid_stuff(boids)
        bx, by = boid.position
        ax, ay = avg_position

        to_center = pt_to_pt_angle_deg(boid.position, avg_position)

        #print(pt_to_pt_angle_deg((100, 100), pygame.mouse.get_pos()))

        dpos = distance(boid.position, avg_position)
        crowded = False
        if dpos < 50:
            crowded = True
            print("crowded")


        # boid likes moving straight.
        # boid likes partners
        # boid dislikes crowd
        # boid dislikes wall

        if crowded:
            dtc = to_center - boid.direction
            if dtc > 0:
                new_rotation = boid.direction + 30
            else:
                new_rotation = boid.direction - 30

        else:
            new_rotation = int(mean([avg_rotation, to_center]))

        boid.rotate(new_rotation)
      
    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))

    pygame.display.flip()
    fpsClock.tick(fps)
