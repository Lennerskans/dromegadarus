
import os
import pygame
import random
import sys

import config
import gfxlib

pygame.init()


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def intro_background(display):
    colors = [
        (0, 0, 128),
        (64, 64, 192),
        (128, 64, 192),
        (192, 64, 128),
        (192, 0, 0),
        (0, 0, 0)
    ]
    for i in range(6):
        slice = pygame.Surface((display.Scale * display.Width, 50 * display.Scale))
        pygame.draw.rect(slice, colors[i], pygame.Rect(0, 0, display.Scale * display.Width, 50 * display.Scale))
        config.intro_slices.append(slice)

    config.scroll = pygame.Surface((display.Scale * display.Width * 9, 20 * display.Scale))
    blob1 = gfxlib.draw_string_surface(display.Scale, 'DROMEGADARUS', True)
    blob2 = gfxlib.draw_string_surface(display.Scale, '@JOACHIM LENNERSKANS 2022')
    blob3 = gfxlib.draw_string_surface(display.Scale, 'USE LEFT CTRL AND ARROWS')
    blob4 = gfxlib.draw_string_surface(display.Scale, 'PRESS THE ANY KEY')
    config.scroll.fill((0, 0, 0))
    config.scroll.blit(blob1, (display.Scale * 240 * 1, display.Scale * 2))
    config.scroll.blit(blob2, (display.Scale * 240 * 2, display.Scale * 6))
    config.scroll.blit(blob1, (display.Scale * 240 * 3, display.Scale * 2))
    config.scroll.blit(blob3, (display.Scale * 240 * 4, display.Scale * 6))
    config.scroll.blit(blob1, (display.Scale * 240 * 5, display.Scale * 2))
    config.scroll.blit(blob4, (display.Scale * 240 * 6, display.Scale * 6))
    
def background(display):
    colors = [
        (255, 64, 0),
        (255, 64, 0),
        (255, 64, 0),
        (255, 128, 64),
        (255, 128, 64),
        (255, 128, 64),
        (255, 128, 64),
        (255, 192, 64),
        (255, 192, 64),
        (255, 192, 64),
        (64, 128, 64),
        (64, 128, 64),
        (64, 128, 64),
        (64, 192, 64),
        (64, 192, 64),
        (64, 192, 64),
        (64, 192, 64),
        (64, 255, 64),
        (64, 255, 64),
        (64, 255, 64)
        ]

    for y in range(display.Height):
        for x in range(display.Width):
            i = 0 if x % 2 == y % 2 else 1
            if y < 60:
                j = int(y / 12) * 2
            else:
                j = int((y - 60) / 20) * 2 + 10
            
            pygame.draw.rect(display.Screen, colors[j + i], 
                pygame.Rect(display.x(x), display.y(y), display.h(1), display.w(1)))

    config.background_screen = display.Screen.subsurface(
        pygame.Rect(display.x(0), display.y(0), display.w(display.Width), display.h(display.Height))
        ).copy()
    pygame.display.flip()

def toggle(map, y, x, char):
    if map[y][x] == 'X':
        return map
    elif char == '/' and map[y][x] == '\\':
        map[y][x] = 'V'
    elif char == '\\' and map[y][x] == '/':
        map[y][x] = 'V'
    else:
        map[y][x] = char

    return map

def mountains(display):
    mountain_width = 90
    config.mountain_gfx = pygame.Surface(((mountain_width + 30) * 8 * display.Scale, 72 * display.Scale))
    slice = config.background_screen.subsurface(pygame.Rect(0, 4 * display.Scale, 8 * display.Scale, 72 * display.Scale))
    for x in range(mountain_width + 30):
        config.mountain_gfx.blit(slice, (x * 8 * display.Scale, 0))

    character_lookup = {
        'X': 58,
        'V': 59,
        '/': 56,
        '\\': 57
    }

    # Create three levels of mountains at random
    character_offset = [0, -12, 4]
    heights = [7, 6, 5]
    numbers = [12, 10, 8]
    for level in range(3):
        map = []
        for y in range(7):
            map.append([])
            for x in range(mountain_width):
                map[y].append('.')

        for mountain in range(numbers[level]):
            height = random.randrange(2, heights[level] + 1)
            midx = random.randrange(height - 1, mountain_width - height)
            for i in range(height):
                y = 7 - height + i
                map = toggle(map, y, midx - i, '/')
                map = toggle(map, y, midx + i + 1, '\\')
                for x in range(i):
                    map = toggle(map, y, midx - x, 'X')
                    map = toggle(map, y, midx + x + 1, 'X')

        # Blit mountains
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == '.':
                    continue
                char = config.characters[character_lookup[map[y][x]] + character_offset[level]]
                config.mountain_gfx.blit(char, (x * 8 * display.Scale, (y + level) * 8 * display.Scale))
                if x < 30:
                    config.mountain_gfx.blit(char, ((90 + x) * 8 * display.Scale, (y + level) * 8 * display.Scale))



def load(display):
    # Scale all gfx up with scale

    # Character set
    character_url = resource_path('images/Charset.png')
    character = pygame.image.load(character_url)
    for y in range(4):
        for x in range(16):
            onechar = character.subsurface(pygame.Rect(x * 8, y * 8, 8, 8))
            bigchar = pygame.transform.scale(onechar, (8 * display.Scale, 8 * display.Scale))
            config.characters.append(bigchar)
            biggerchar = pygame.transform.scale(onechar, (2 * 8 * display.Scale, 2 * 8 * display.Scale))
            config.big_characters.append(biggerchar)
    pygame.display.flip()

    # Intro
    intro_background(display)

    # Background
    background(display)
    mountains(display)

    # Dromedaries
    dromedary_url = resource_path('images/Dromedary.png')
    dromedary_pic = pygame.image.load(dromedary_url)
    for x in range(6):
        dromedary = dromedary_pic.subsurface(pygame.Rect(x * 32, 0, 32, 24))
        big_dromedary = pygame.transform.scale(dromedary, (32 * display.Scale, 24 * display.Scale))
        config.dromedaries.append(big_dromedary)
    pygame.display.flip()

    # Explosion
    explosion_url = resource_path('images/ExplodingCamel.png')
    explosion_pic = pygame.image.load(explosion_url)
    for x in range(8):
        exploding_camel = explosion_pic.subsurface(pygame.Rect(x * 16, 0, 16, 16))
        big_exploding_camel = pygame.transform.scale(exploding_camel, (16 * display.Scale, 16 * display.Scale))
        config.exploding_camels.append(big_exploding_camel)

    # Lightning
    lightning_url = resource_path('images/Blixt.png')
    lightning_pic = pygame.image.load(lightning_url)
    for y in range(6):
        lightning = lightning_pic.subsurface(pygame.Rect(0, y * 5, 14, 5))
        big_lightning = pygame.transform.scale(lightning, (14 * display.Scale, 5 * display.Scale))
        config.lightning.append(big_lightning)

    
