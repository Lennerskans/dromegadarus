import pygame
import setup
import time

import config


def intro(display):
    clock = pygame.time.Clock()

    display.Screen.fill((0, 0, 0))
    pygame.display.flip()

    music_url = setup.resource_path('sounds\\goblinsshort.wav')
    pygame.mixer.music.load(music_url)
    pygame.mixer.music.play(-1)

    SPEED = 1.02
    FRAMERATE = 20
    frame_no = 0
    lines = []
    line_colors = []
    next_line_color = 4
    SEED = 0.5
    seed = SEED
    for i in range(15):
        lines.append(seed)
        seed *= SPEED ** FRAMERATE
        line_colors.append(i % 5)

    black_border_h = 18
    black_border_y = int((display.Height - black_border_h) / 2)

    counter = 0

    running = True
    play = True
    while running:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                running = False   
            if event.type == pygame.KEYDOWN:
                running = False

        # Move lines
        frame_no += 1
        for i in range(len(lines)):
            lines[i] *= SPEED
        if frame_no == FRAMERATE:
            frame_no = 0
            lines.pop()
            line_colors.pop()
            lines.insert(0, SEED)            
            line_colors.insert(0, next_line_color)
            next_line_color -= 1
            if next_line_color == -1:
                next_line_color = 4

        counter += 1
        if counter >= 7 * display.Width:
            counter = 0
        scroll_subsurface = config.scroll.subsurface(pygame.Rect(counter * display.Scale, 0, display.Width * display.Scale, 16 * display.Scale)).copy()
        display.Screen.blit(scroll_subsurface, (display.x(0), display.y(black_border_y)))

        # Colored lines
        y1 = int(lines[0])
        for i in range(len(lines) - 1):
            y2 = int(lines[i +1]) - 1
            if y2 > y1:                
                yl1 = black_border_y + black_border_h + y1
                yl2 = black_border_y + black_border_h + y2 - 1
                if yl2 >= display.Height:
                    yl2 = display.Height - 1
                if yl2 >= yl1:
                    block = config.intro_slices[line_colors[i]].subsurface(pygame.Rect(0, 0, display.Width * display.Scale, (yl2 - yl1 + 1) * display.Scale)).copy()
                    display.Screen.blit(block, (display.x(0), display.y(yl1)))

                yl1 = black_border_y - y2 + 1
                yl2 = black_border_y - y1
                if yl1 < 0:
                    yl1 = 0
                if yl2 >= yl1:
                    block = config.intro_slices[line_colors[i]].subsurface(pygame.Rect(0, 0, display.Width * display.Scale, (yl2 - yl1 + 1) * display.Scale)).copy()
                    display.Screen.blit(block, (display.x(0), display.y(yl1)))

                y1 = y2

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()

    return play



