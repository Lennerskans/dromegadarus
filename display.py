import pygame

pygame.init()

WIDTH = 240
HEIGHT = 160

class Display:
    Width = 0
    Height = 0 
    MaxWidth = 0
    MaxHeight = 0
    Offset_X = 0
    Offset_Y = 0
    Scale = 0
    Screen = None

    # ToDo: add screen here
    def __init__(self, width, height):
        self.Width = width 
        self.Height = height 
        self.Offset_X = 0
        self.Offset_Y = 0
        self.Scale = 0

    def x(self, x):
        return x * self.Scale + self.Offset_X

    def y(self, y):
        return y * self.Scale + self.Offset_Y

    def h(self, height):
        return height * self.Scale

    def w(self, width):
        return width * self.Scale

  


def setup_window(screen, selected_scale, max_scale):
    display = Display(WIDTH, HEIGHT)
    display.Scale = min(selected_scale, max_scale)
    
    if(selected_scale > max_scale):
        # Full screen
        display.Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display.MaxWidth, display.MaxHeight = pygame.display.Info().current_w, pygame.display.Info().current_h         
        display.Offset_X = (display.MaxWidth - display.Width * max_scale) / 2
        display.Offset_Y = (display.MaxHeight - display.Height * max_scale) / 2
        display.Screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(display.Offset_X, display.Offset_Y, display.Scale * display.Width, display.Scale * display.Height))
    else:
        display.MaxWidth = selected_scale * display.Width
        display.MaxHeight = selected_scale * display.Height
        display.Screen = pygame.display.set_mode((display.MaxWidth, display.MaxHeight))
        display.Screen.fill((255,255,255))
        display.Offset_X = display.Offset_Y = 0

    sysfont = pygame.font.SysFont('Arial Bold', 20)
    textsurface = sysfont.render('Press +/- to change screen size, ENTER to chose.', True, (0, 0, 0))
    display.Screen.blit(textsurface, (display.Offset_X + 10, display.Offset_Y + 10))

    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
        display.Offset_X + (display.Width - 5) * display.Scale, 
        display.Offset_Y + (display.Height - 5) * display.Scale, 
        5 * display.Scale, 
        5 * display.Scale))

    pygame.display.flip()

    return display

def calibrate_screensize():
    # Find out max resolution, and from that max scale
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    max_width, max_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    scale_x = int(max_width / WIDTH)
    scale_y = int(max_height / HEIGHT)
    max_scale = min(scale_x, scale_y)

    # Let the user decide window size
    selected_scale = max_scale + 1  # Full screen is max_scale with offset

    finished = False
    while not finished:
        display = setup_window(screen, selected_scale, max_scale)

        waiting_for_keypress = True
        while waiting_for_keypress:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS and selected_scale <= max_scale:
                        selected_scale += 1
                        waiting_for_keypress = False
                    if event.key == pygame.K_MINUS and selected_scale > 1:
                        selected_scale -= 1
                        waiting_for_keypress = False
                    if event.key == pygame.K_RETURN:
                        waiting_for_keypress = False
                        finished = True

    return display

