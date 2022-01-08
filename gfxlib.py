import pygame

import config
import display

def character_lookup(ascii):
    char_code = 0
    if 48 <= ascii <= 57:
        char_code = ascii - 48 + 32 # Number 0=ascii 48, 32 in my charset
    elif 65 <= ascii <= 90:
        char_code = ascii - 65
    elif ascii == 63: # ?
        char_code = 26
    elif ascii == 64: # @
        char_code = 48
    elif ascii == 47: # /
        char_code = 27
    elif ascii == 33: # !
        char_code = 28
    elif ascii == 32: # [SPACE]
        char_code = 29

    return char_code

def draw_string_surface(scale, string, big_characters = False):
    w = scale * len(string) * 8
    h = 8 * scale
    if big_characters:
        w *= 2
        h *= 2

    surface = pygame.Surface((w, h))
    
    for x in range(len(string)):
        ascii = ord(string[x])
        char_code = character_lookup(ascii)

        if big_characters:
            surface.blit(config.big_characters[char_code], (x * 8 * scale * 2, 0))
        else:
            surface.blit(config.characters[char_code], (x * 8 * scale, 0))

    return surface


# Could reuse draw_string_surface
def draw_string(offset_x, y, string, display, big_characters = False):
    for x in range(len(string)):
        ascii = ord(string[x])
        char_code = character_lookup(ascii)

        if big_characters:
            display.Screen.blit(config.big_characters[char_code], (display.x(offset_x + x * 8 * 2), display.y(y)))
        else:
            display.Screen.blit(config.characters[char_code], (display.x(offset_x + x * 8), display.y(y)))

