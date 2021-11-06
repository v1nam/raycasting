import pygame
import json
import math

gmap = []
path = ""
map_dims = []

if input("new file? (y/n): ").lower() == 'y':
    path = input("path to save file to: ")
    map_dims = [int(input("enter map width: ")), int(input("enter map height: "))]
    gmap = [[0 for x in range(map_dims[0])] for y in range(map_dims[1])]
elif (path := input("path to load existing file: ")):
    with open(path, "r") as f:
        gmap = json.load(f)
        map_dims = [len(gmap[0]), len(gmap)]

pygame.init()

screen = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()

r = True

RED = (191, 97, 106)
GREEN = (163, 190, 140)
BLUE = (94, 129, 172)
WHITE = (236, 239, 244)
YELLOW = (235, 203, 139)

colarr = {
    1: RED,
    2: GREEN,
    3: BLUE,
    4: WHITE,
    5: YELLOW,
}

w, h = screen.get_size()

gridsurf = pygame.Surface((w, h))
gridsurf.fill((46, 52, 64))
rw, rh = w / map_dims[0], h / map_dims[1]
for x in range(map_dims[0]):
    for y in range(map_dims[1]):
        pygame.draw.rect(gridsurf, (59, 66, 82), (x * rw, y * rh, math.ceil(rw), math.ceil(rh)), 1)
        if (mapval := gmap[y][x]):
            pygame.draw.rect(gridsurf, colarr[mapval], (x * rw + 1, y * rh + 1, math.ceil(rw) - 2, math.ceil(rh) - 2))

def change_map(mx, my, val, col):
    try:
        gmap[int(my / rh)][int(mx / rw)] = val
    except IndexError:
        print(int(my / rh), int(my / rw))
        exit()
    pygame.draw.rect(gridsurf, col, ((mx // rw) * rw + 1, (my // rh) * rh + 1, rw - 2, rh - 2))

current_col = 2

while r:
    screen.fill((46, 52, 64))
    screen.blit(gridsurf, (0, 0))
    mx, my = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (76, 86, 106), ((mx // rw) * rw + 1, (my // rh) * rh + 1, rw - 2, rh - 2))
    if mx <= w and mx >= 0 and my <= h and my >= 0:
        if pygame.mouse.get_pressed()[0]:
            change_map(mx, my, current_col, colarr[current_col])
        elif pygame.mouse.get_pressed()[2]:
            change_map(mx, my, 0, (46, 52, 64))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        current_col = 1
    if keys[pygame.K_2]:
        current_col = 2
    if keys[pygame.K_3]:
        current_col = 3
    if keys[pygame.K_4]:
        current_col = 4
    if keys[pygame.K_5]:
        current_col = 5

    if keys[pygame.K_s]:
        with open(path, "w") as m:
            json.dump(gmap, m)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
            break
    pygame.display.update()
    clock.tick(60)
pygame.quit()