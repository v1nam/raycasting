import pygame
import json

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((700, 450))

gmap = []
with open(input("path of map file to load: "), "r") as m:
    gmap = json.load(m)

running = True
w, h = screen.get_size()

MINIMAP_SCALE_FACTOR = 4
MINIMAP_SIZE = (len(gmap[0]) * MINIMAP_SCALE_FACTOR, len(gmap) * MINIMAP_SCALE_FACTOR)

clock = pygame.time.Clock()
fp = 0

myfont = pygame.font.Font("font/yoster.ttf", 20)

RED = (191, 97, 106)
GREEN = (163, 190, 140)
BLUE = (94, 129, 172)
WHITE = (236, 239, 244)
YELLOW = (235, 203, 139)

DARK_RED = (156, 64, 73)
DARK_GREEN = (127, 161, 98)
DARK_BLUE = (55, 88, 130)
GRAY = (216, 222, 233)
DARK_YELLOW = (181, 150, 87)

DARK_GRAY = (59, 66, 82)
SKY_BLUE = (129, 161, 193)
BLACK = (46, 52, 64)
ORANGE = (208, 135, 112)


class Player:
    def __init__(self, gmap):
        self.pos = pygame.Vector2(2, 2)
        self.dir = pygame.Vector2(1, 0)  # direction relative to player position
        self.camera_plane = pygame.Vector2(
            0, -0.66
        )  # camera plane perpendicular to direction
        self.gmap = gmap

        self.colarr = {
            1: RED,
            2: GREEN,
            3: BLUE,
            4: WHITE,
            5: YELLOW,
        }

        self.shadearr = {
            1: DARK_RED,
            2: DARK_GREEN,
            3: DARK_BLUE,
            4: GRAY,
            5: DARK_YELLOW,
        }

        self.MOVE_SPEED = 4  # blocks per sec
        self.ROT_SPEED = 3  # radians per sec

    def handle_input(self, fp):
        speed = fp * self.MOVE_SPEED
        rot_sp = fp * self.ROT_SPEED
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if not self.gmap[int(self.pos.x + self.dir.x * speed)][
                int(self.pos.y)
            ]:  # check for wall collision
                self.pos.x += self.dir.x * speed
            if not self.gmap[int(self.pos.x)][int(self.pos.y + self.dir.y * speed)]:
                self.pos.y += self.dir.y * speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if not self.gmap[int(self.pos.x - self.dir.x * speed)][int(self.pos.y)]:
                self.pos.x -= self.dir.x * speed
            if not self.gmap[int(self.pos.x)][int(self.pos.y - self.dir.y * speed)]:
                self.pos.y -= self.dir.y * speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dir = self.dir.rotate_rad(rot_sp)
            self.camera_plane = self.camera_plane.rotate_rad(rot_sp)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dir = self.dir.rotate_rad(-rot_sp)
            self.camera_plane = self.camera_plane.rotate_rad(-rot_sp)

    def raycast(self, w, h, screen):
        for x in range(0, w, 3):
            cx = 2 * x / w - 1  # map x-w to 0-1
            ray_dir = pygame.Vector2(
                self.dir.x + self.camera_plane.x * cx,
                self.dir.y + self.camera_plane.y * cx,
            )
            map_pos = pygame.Vector2(int(self.pos.x), int(self.pos.y))
            delx = abs(1 / ray_dir.x) if ray_dir.x != 0 else 1e30
            dely = abs(1 / ray_dir.y) if ray_dir.y != 0 else 1e30
            # dist travelled by ray from the player position, incremented side by side, see http://www.cse.yorku.ca/~amana/research/grid.pdf
            side_dist = pygame.Vector2()
            hit = False
            step = pygame.Vector2()
            side_dir = 0
            if ray_dir.x < 0:
                step.x = -1
                side_dist.x = (self.pos.x - map_pos.x) * delx
            else:
                step.x = 1
                side_dist.x = (map_pos.x + 1 - self.pos.x) * delx
            if ray_dir.y < 0:
                step.y = -1
                side_dist.y = (self.pos.y - map_pos.y) * dely
            else:
                step.y = 1
                side_dist.y = (map_pos.y + 1 - self.pos.y) * dely

            while not hit:
                if side_dist.x < side_dist.y:
                    map_pos.x += step.x
                    side_dist.x += delx
                    side_dir = 0
                else:
                    map_pos.y += step.y
                    side_dist.y += dely
                    side_dir = 1
                if self.gmap[int(map_pos.x)][int(map_pos.y)] > 0:
                    hit = True

            ray_dist = side_dist.y - dely if side_dir else side_dist.x - delx
            line_height = int(h * 1.5 / ray_dist)
            upper_wall = int(h / 2 - line_height / 2)
            lower_wall = int(h / 2 + line_height / 2)
            upper_wall = max(0, upper_wall)
            lower_wall = min(h - 1, lower_wall)
            col = (self.colarr if not side_dir else self.shadearr).get(
                self.gmap[int(map_pos.x)][int(map_pos.y)]
            )
            pygame.draw.line(screen, DARK_GRAY, (x, lower_wall), (x, h), 3)
            pygame.draw.line(screen, col, (x, upper_wall), (x, lower_wall), 3)
            minimap_player_pos = (
                self.pos.y * MINIMAP_SCALE_FACTOR,
                self.pos.x * MINIMAP_SCALE_FACTOR,
            )
            # pygame.draw.line(
            #     raysurf,
            #     (*GREEN, 150),
            #     minimap_player_pos,
            #     minimap_player_pos
            #     + pygame.Vector2(
            #         ray_dir.y * ray_dist * MINIMAP_SCALE_FACTOR,
            #         ray_dir.x * ray_dist * MINIMAP_SCALE_FACTOR,
            #     ),
            # )


player = Player(gmap)
minimap = pygame.Surface(MINIMAP_SIZE)
minimap.fill(BLACK)
for i, arr in enumerate(gmap):
    for j, my in enumerate(arr):
        if my > 0:
            pygame.draw.rect(
                minimap,
                player.colarr[my],
                (
                    MINIMAP_SCALE_FACTOR * j,
                    MINIMAP_SCALE_FACTOR * i,
                    MINIMAP_SCALE_FACTOR,
                    MINIMAP_SCALE_FACTOR,
                ),
            )
raysurf = pygame.Surface(MINIMAP_SIZE, pygame.SRCALPHA, 32).convert_alpha()

while running:
    screen.fill(SKY_BLUE)
    raysurf.fill((0, 0, 0, 0))

    player.raycast(w, h, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    player.handle_input(fp)

    fpstext = myfont.render(str(int(clock.get_fps())), False, BLACK)
    screen.blit(fpstext, (10, 10))
    screen.blit(minimap, (w - MINIMAP_SIZE[0], h - MINIMAP_SIZE[1]))
    screen.blit(raysurf, (w - MINIMAP_SIZE[0], h - MINIMAP_SIZE[1]))
    pygame.draw.circle(
        screen,
        ORANGE,
        (
            (w - MINIMAP_SIZE[0]) + player.pos.y * MINIMAP_SCALE_FACTOR,
            (h - MINIMAP_SIZE[1]) + player.pos.x * MINIMAP_SCALE_FACTOR,
        ),
        2,
    )
    pygame.display.update()
    fp = clock.tick(60) / 1000
pygame.quit()
