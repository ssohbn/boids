import sys
import pygame
from math import radians, degrees, sin, cos, atan, sqrt
from random import randint
from numpy import mean
from pygame.font import SysFont

def angle_move_thing(position: tuple[int, int], direction: int, amount: int) -> tuple[float, float]:
    x,y = position
    r_direction = radians(direction)

    x = x + (cos(r_direction) * amount)
    y = y - (sin(r_direction) * amount)
    return (x, y)

class Boid:
    def __init__(self, direction: int, position: tuple[int, int], speed: int):
        self.direction: int = direction
        self.position: tuple[int, int] = position
        self.speed: int = speed

    def rotate(self, direction: int):
        self.direction = direction


    def move(self):
        x, y = angle_move_thing(self.position, self.direction, self.speed)
        self.position = int(x), int(y)

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

def average_boid_stuff(boids: list[Boid]) -> tuple[int, tuple[int, int], int]:
    speeds = []

    rotations = [] # THE PESKY EVIL I WAS SEARCHING FOR. THIS IS THE BUG. HOLY OOPSIE DAISY OHMY GOSH
    xs = []
    ys = []
    for boid in boids:
        rotations.append(boid.direction)
        xs.append(boid.position[0])
        ys.append(boid.position[1])
        speeds.append(boid.speed)

    return int(mean(rotations)), (int(mean(xs)), int(mean(ys))), int(mean(speeds))


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
pygame.font.init()
default_font_name = pygame.font.get_default_font()
font = pygame.font.SysFont(default_font_name, 24)

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

boids = make_some_boids(3, (width, height), 10)

# Game loop.
while True:
    screen.fill((255,255,255))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    for boid in boids:
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            break

        boid.move()

        avg_rotation, avg_position, avg_speed = average_boid_stuff(boids)

        TEST_POS = (300, 300) # replace with avg pos later
        avg_position = TEST_POS

        avg_boid_goal = angle_move_thing(avg_position, avg_rotation, avg_speed)

        dist = distance(boid.position, avg_position)
        CROWD_DISTANCE = 1
        #to_center_weight =  dist / CROWD_DISTANCE# the farther the fish are, the more they wanna go to the center
        to_center_weight = 0
        to_heading_weight= 1 - to_center_weight

        # weights die
        # evil.
        goal_x = int(mean([avg_boid_goal[0] * to_heading_weight, avg_position[0] * to_center_weight])) 
        goal_y = int(mean([avg_boid_goal[1] * to_heading_weight, avg_position[1] * to_center_weight]))
        goal_position = goal_x, goal_y

        new_rotation = pt_to_pt_angle_deg(boid.position, goal_position)

        pygame.draw.line(screen, (0, 255, 0), avg_position, (boid.position))
        pygame.draw.line(screen, (0, 0, 255), avg_boid_goal, (boid.position))
        pygame.draw.line(screen, (255, 0, 0), goal_position, boid.position)

        boid.rotate(new_rotation) # use new_rotation once weights arent.. zero..
        print(new_rotation)

        # print(f"avg_goal: {avg_boid_goal}")
        # print(f"to heading: {to_average_weight}")
        # print(f"to center: {to_center_weight}")


    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))
        pygame.draw.line(screen, (0, 0, 0), angle_move_thing(boid.position, boid.direction, 50), boid.position)

    pygame.display.flip()
    fpsClock.tick(fps)
