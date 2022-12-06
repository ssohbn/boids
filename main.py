import sys
import pygame
from math import radians, degrees, sin, cos, atan, sqrt
from random import randint
from numpy import mean

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

def make_some_boids(amount: int, grid_dimensions: tuple[int, int], speed: int = 5, randomize_speed: bool = False) -> list[Boid]:
    boids = []

    if randomize_speed:
        for _ in range(amount):
            boids.append(Boid(randint(0, 360), (randint(0, grid_dimensions[0]), randint(0, grid_dimensions[1])), randint(3, speed)))
    else:
        for _ in range(amount):
            boids.append(Boid(randint(0, 360), (randint(0, grid_dimensions[0]), randint(0, grid_dimensions[1])), speed))

    return boids

def average_boid_stuff(boids: list[Boid]) -> tuple[int, tuple[int, int], int]:
    speeds = []

    xs = []
    ys = []

    gxs = []
    gys = []

    for boid in boids:
        xs.append(boid.position[0])
        ys.append(boid.position[1])
        speeds.append(boid.speed)

        gx, gy = angle_move_thing(boid.position, boid.direction, boid.speed)
        gxs.append(gx - boid.position[0]) # getting offset from zero by subtracting original thing?
        gys.append(gy - boid.position[1]) # i dont know vector math so i dont know if this will affect the angle but surely it cant harm it


    avg_rotation = pt_to_pt_angle_deg((0,0), (int(mean(gxs)), int(mean(gys))))

    avg_position = (int(mean(xs)), int(mean(ys)))
    avg_speed = int(mean(speeds))

    return avg_rotation, avg_position, avg_speed

def bounded(x: int, lower_bound: int, upper_bound: int) -> int:
    if x < lower_bound:
        x = lower_bound
    if x > upper_bound:
        x = upper_bound

    return x

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
pygame.font.init()
default_font_name = pygame.font.get_default_font()
font = pygame.font.SysFont(default_font_name, 24)

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

BOID_COUNT = 100
boids = make_some_boids(100, (width, height), randomize_speed=True, speed = 10)

# Game loop.
while True:
    screen.fill((255,255,255))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    avg_direction, avg_position, avg_speed = average_boid_stuff(boids)
    #avg_position = (300, 300)

    for boid in boids:
        avg_goal = angle_move_thing(boid.position, avg_direction, boid.speed)

        dist = distance(boid.position, avg_position)
        CROWD_DISTANCE = 50
        AVOID_DISTANCE = 5

        to_center_weight = .2 #dist / CROWD_DISTANCE % CROWD_DISTANCE
        avoid_weight = 1 #dist / AVOID_DISTANCE % AVOID_DISTANCE
        keep_moving_weight = 1 #1
        to_heading_weight= 1 #1 - to_center_weight
        wiggle_weight = 1

        weights = to_center_weight + to_heading_weight + avoid_weight + keep_moving_weight + wiggle_weight
        print(weights)


        goal_x = int(sum([
            avg_goal[0] * to_heading_weight,
            avg_position[0] * to_center_weight,
            boid.direction * keep_moving_weight,
            (boid.direction+180) * avoid_weight,
            boid.direction + randint(-180, 180) * wiggle_weight,
        ])/weights)

        goal_y = int(sum([avg_goal[1] * to_heading_weight,
            avg_position[1] * to_center_weight,
            boid.direction * keep_moving_weight,
            (boid.direction+180) * avoid_weight,
            boid.direction + randint(-180, 180) * wiggle_weight,
        ])/weights)

        goal_position = goal_x, goal_y

        new_rotation = pt_to_pt_angle_deg(boid.position, goal_position)

        pygame.draw.line(screen, (0, 255, 0), avg_position, (boid.position))
        pygame.draw.line(screen, (0, 0, 255), avg_goal, (boid.position))
        pygame.draw.line(screen, (255, 0, 0), goal_position, boid.position)

        boid.rotate(new_rotation) # use new_rotation once weights arent.. zero..

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            boid.move()

    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))
        pygame.draw.line(screen, (0, 0, 0), angle_move_thing(boid.position, boid.direction, 50), boid.position)
        screen.blit(font.render(f"avg_position: {avg_position}", False, (0, 0, 0)), avg_position)

    pygame.display.flip()
    fpsClock.tick(fps)
