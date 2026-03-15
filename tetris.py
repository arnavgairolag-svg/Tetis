# import libraries
import pygame
import sys
from random import choice, randrange
from copy import deepcopy

# initialize
pygame.init()

# game screen setup
WIDTH, HEIGHT = 10, 19
tile = 45

game_resolution = WIDTH * tile, HEIGHT * tile
resolution = 750, 940
FPS = 60

window = pygame.display.set_mode(resolution)
screen = pygame.Surface(game_resolution)
pygame.display.set_caption("Tetris")

# pastel color palette
black = (20, 20, 25)
white = (245, 245, 245)

pastel_purple = (210, 190, 235)
pastel_green  = (170, 220, 190)
pastel_orange = (235, 170, 120)
pastel_blue   = (180, 210, 235)
pastel_pink   = (235, 180, 210)
pastel_yellow = (235, 225, 170)

PASTEL_COLORS = [
    pastel_purple,
    pastel_green,
    pastel_orange,
    pastel_blue,
    pastel_pink,
    pastel_yellow
]

# clocks and fonts
clock = pygame.time.Clock()
title_font = pygame.font.Font("C:/Pygame/Tetris/font.ttf", 65)
main_font = pygame.font.Font("C:/Pygame/Tetris/font.ttf", 50)
font = pygame.font.Font("C:/Pygame/Tetris/font.ttf", 45)

# titles
title_tetris = title_font.render("TETRIS", True, pastel_orange)
title_score  = main_font.render("SCORE:", True, pastel_green)
title_record = main_font.render("RECORD:", True, pastel_purple)

# grid setup
grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(WIDTH) for y in range(HEIGHT)]

# figure setup
figures_position = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],      # I
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],    # O
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],     # S
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],     # Z
    [(0, 0), (0, -1), (0, 1), (-1, -1)],     # L
    [(0, 0), (1, 0), (0, -1), (-1, -1)],     # J
    [(0, 0), (0, -1), (0, 1), (-1, 0)]       # T
]

figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in figure_pos] for figure_pos in figures_position]
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]

animation_count, animation_speed, animation_limit = 0, 60, 2000

# soft pastel tile colors
get_color = lambda: choice(PASTEL_COLORS)

# next figure
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

# score setup
score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# backgrounds
window_background = pygame.image.load("C:/Pygame/Tetris/bg.jpg").convert()
screen_background = pygame.image.load("C:/Pygame/Tetris/bg2.jpg").convert()

# functions
def check_borders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > WIDTH - 1:
            return False
        elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
            return False
    return True

def get_record():
    try:
        with open("record") as f:
            return int(f.readline().strip())
    except (FileNotFoundError, ValueError):
        with open("record", "w") as f:
            f.write("0")
        return 0

def set_record(score):
    record = get_record()
    if score > record:
        with open("record", "w") as f:
            f.write(str(score))

def draw_block(surface, color, rect):
    pygame.draw.rect(surface, color, rect, border_radius=8)  # rounded edges

# gameloop
running = True
while running:
    records = get_record()
    dx, rotate = 0, False
    window.blit(window_background, (0, 0))
    window.blit(screen, (20, 20))
    screen.blit(screen_background, (0, 0))
    
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                dx = -1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dx = 1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                animation_limit = 100
            elif event.key in (pygame.K_UP, pygame.K_w):
                rotate = True
    
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    
    # move y
    animation_count += animation_speed
    if animation_count > animation_limit:
        animation_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                animation_limit = 2000
                break
    
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
        if not check_borders():
            figure = deepcopy(figure_old)
    
    # check lines
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            animation_speed += 3
            lines += 1
    
    # award points
    score += scores[lines]
    
    # draw grid
    for i in grid:
        pygame.draw.rect(screen, (60, 60, 70), i, 1)
    
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        # shadow
        shadow_rect = figure_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=8)
        # block
        draw_block(screen, color, figure_rect)
    
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * tile, y * tile
                draw_block(screen, col, figure_rect)
    
    # draw next figures
    for i in range(4):
        figure_rect.x = next_figure[i].x * tile + 380
        figure_rect.y = next_figure[i].y * tile + 185
        draw_block(window, next_color, figure_rect)
    
    # ================== UI (BOTTOM RIGHT) ==================
    PANEL_X = resolution[0] - 140
    PANEL_BOTTOM = resolution[1] - 40
    GAP = 66

    # TETRIS
    window.blit(title_tetris, (resolution[0] - 265, 10))

    # RECORD
    record_title_rect = title_record.get_rect(center=(PANEL_X - 10, PANEL_BOTTOM - GAP*3.4))
    record_value_rect = font.render(str(records), True, (255, 220, 150)).get_rect(
        center=(PANEL_X - GAP, PANEL_BOTTOM - GAP*2.5)
    )
    window.blit(title_record, record_title_rect)
    window.blit(font.render(str(records), True, (255, 220, 150)), record_value_rect)

    # SCORE
    score_title_rect = title_score.get_rect(center=(PANEL_X - 32, PANEL_BOTTOM - GAP*1.4))
    score_value_rect = font.render(str(score), True, white).get_rect(
        center=(PANEL_X - GAP*1.4, PANEL_BOTTOM - 34)
    )
    window.blit(title_score, score_title_rect)
    window.blit(font.render(str(score), True, white), score_value_rect)


    
    # game over
    for i in range(WIDTH):
        if field[0][i]:
            set_record(score)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            animation_count, animation_speed, animation_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                draw_block(screen, get_color(), i_rect)
                window.blit(screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)
    
    pygame.display.flip()
    clock.tick(FPS)