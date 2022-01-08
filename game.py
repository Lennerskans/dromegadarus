
import pygame

import intro
import mainloop
import setup
import display

pygame.init()

display = display.calibrate_screensize()
setup.load(display)

while True:
    if not intro.intro(display):
        break
    if not mainloop.game(display):
        break
