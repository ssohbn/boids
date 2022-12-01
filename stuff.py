from random import randint
from math import radians, degrees, sin, cos, atan, sqrt
from numpy import mean
from boid import Boid

def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay
    return int(sqrt(dx ** 2 + dy ** 2))

def make_some_boids(amount: int, grid_dimensions: tuple[int, int], speed: int) -> list[Boid]:
    boids = []
    for _ in range(amount):
        boids.append(Boid(randint(0, 360), (randint(0, grid_dimensions[0]), randint(0, grid_dimensions[1])), speed))

    return boids

def average_boid_stuff(boids: list[Boid]) -> tuple[int, tuple[int, int], int]:
    rotations = []
    speeds = []
    xs = []
    ys = []
    for boid in boids:
        rotations.append(boid.direction)
        xs.append(boid.position[0])
        ys.append(boid.position[1])
        speeds.append(boid.speed)

    return int(mean(rotations)), (int(mean(xs)), int(mean(ys))), int(mean(speeds))

def angle_move_thing(position: tuple[int, int], direction: int, amount: int) -> tuple[float, float]:
    x,y = position
    r_direction = radians(direction)

    x = x + (cos(r_direction) * amount)
    y = y - (sin(r_direction) * amount)
    return (x, y)


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
        return 0 # tbh i feel like 90 or -90 degrees is more valid but i dont particularly care
