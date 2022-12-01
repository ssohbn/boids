import sys
import pygame
from math import radians, degrees, sin, cos, atan, sqrt
from numpy import mean

from stuff import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

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
        CROWD_DISTANCE = 5
        to_center_weight = dist%CROWD_DISTANCE/CROWD_DISTANCE# the farther the fish are, the more they wanna go to the center
        to_average_weight = 1 - to_center_weight


        # weights die
        # evil.
        goal_x = int(mean([avg_boid_goal[0] * to_average_weight, avg_position[0] * to_center_weight])) 
        goal_y = int(mean([avg_boid_goal[1] * to_average_weight, avg_position[1] * to_center_weight]))
        goal_position = goal_x, goal_y

        new_rotation = pt_to_pt_angle_deg(boid.position, goal_position)

        pygame.draw.line(screen, (0, 255, 0), avg_position, (boid.position))
        pygame.draw.line(screen, (0, 0, 255), avg_boid_goal, (boid.position))
        pygame.draw.line(screen, (255, 0, 0), goal_position, (boid.position))
        #pygame.draw.rect(screen, (0, 0, 255), (avg_position[0], avg_position[1], 10, 10))
        boid.rotate(new_rotation) # use new_rotation once weights arent.. zero..

        print(avg_position, avg_boid_goal, goal_position)


    # Draw.
    for boid in boids:
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(boid.position[0], boid.position[1], 10, 10))

    pygame.display.flip()
    fpsClock.tick(fps)
