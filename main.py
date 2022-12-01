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
        self.direction = direction


    def move(self):
        x,y = self.position

        direction = radians(self.direction)

        x = x + (cos(direction) * self.speed)
        y = y - (sin(direction) * self.speed)

        self.position = (int(x), int(y)) # this cast may be very annoying in the future


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

        TEST_POS = (300, 300) # replace with avg pos later
        avg_position = TEST_POS

        #to_center = pt_to_pt_angle_deg(avg_position, boid.position)
        to_center = pt_to_pt_angle_deg(boid.position, avg_position)
        pygame.draw.line(screen, (0, 255, 0), avg_position, (boid.position))

        dist = distance(boid.position, avg_position)

        # boid likes moving straight.
        #keep_direction = 1000 / dist
        # boid likes partners
        to_center_weight = 1 * dist # the farther the fish are, the more they wanna go to the center
        # boid dislikes crowd
        change_rotation_weight = 1 / dist + .7
        # boid dislikes wall
        #weights = sum([keep_direction, to_center_weight, change_rotation_weight])

        print(dist, change_rotation_weight)

        new_rotation = int(
                #mean([boid.direction * keep_direction, avg_rotation * change_rotation_weight, to_center * to_center_weight]) / weights
                mean([avg_rotation * change_rotation_weight, to_center * to_center_weight]) / sum([to_center_weight, change_rotation_weight])
                #to_center * to_center_weight / to_center_weight
        )

        boid.rotate(new_rotation) # use new_rotation once weights arent.. zero..

    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))

    pygame.display.flip()
    fpsClock.tick(fps)
