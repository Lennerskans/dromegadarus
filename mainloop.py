from enum import Enum
import os
import pygame

from actors import Enemy
from actors import EnemyMovement
from actors import ExplodingCamel
from actors import Fire
import config
import gfxlib
import setup

pygame.init()

# ToDo: create a sprite class to inherit
def draw_sprite(x, y, sprite_width, sprite_height, sprite, display):
    if y < 0 or y > 145:
        return 
    if x < 0:
        partial_sprite = sprite.subsurface(pygame.Rect(-x * display.Scale, 0, (sprite_width + x) * display.Scale, sprite_height * display.Scale))
        display.Screen.blit(partial_sprite, (display.x(0), display.y(y)))
    elif x < display.Width - sprite_width:
        display.Screen.blit(sprite, (display.x(x), display.y(y)))
    elif x < display.Width:
        partial_sprite = sprite.subsurface(pygame.Rect(0, 0, (display.Width - x) * display.Scale, sprite_height * display.Scale))
        display.Screen.blit(partial_sprite, (display.x(x), display.y(y)))

def collide(margin, x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + margin > x2 and x1 + margin < x2 + w2 and y1 + margin > y2 and y1 + margin < y2 + h2:
        return True
    if x1 + margin > x2 and x1 + margin < x2 + w2 and y1 + h1 - margin > y2 and y1 + h1 - margin < y2 + h2:
        return True
    if x1 + w1 - margin > x2 and x1 + w1 - margin < x2 + w2 and y1 + margin > y2 and y1 + margin < y2 + h2:
        return True
    if x1 + w1 - margin > x2 and x1 + w1 - margin < x2 + w2 and y1 + h1 - margin > y2 and y1 + h1 - margin < y2 + h2:
        return True
    return False

def game(display):
    running = True
    game_over = False
    play_again = True
    target_score = 0
    score = 0

    display.Screen.fill((0,0,0)) # Needed if full screen
    clock = pygame.time.Clock()

    # Mountain
    mountain_x = 0
    mountain_delay = 0
    MOUNTAIN_SPEED = 4

    # Player
    PLAYER_X = 8
    player_y = 100
    player_delay = 0
    player_picture = 0
    PLAYER_ANIMATE = 8
    up_held = False
    down_held = False
    player_alive = True
    player_dead_count = 96

    # Fire
    fires = []
    NUMBER_OF_FIRE_MAX = 5
    fire_held = False
    fire_away = False
    fire_sound = pygame.mixer.Sound(setup.resource_path('sounds/fire.wav'))

    # Enemies
    enemies = []
    number_of_enemies = 3
    ENEMY_INCREASE = 180
    enemy_increase_rate = 0
    NUMBER_OF_ENEMIES_MAX = 8
    enemy_movement = EnemyMovement.straight
    enemies_speed = 1
    for x in range(number_of_enemies):
        enemies.append(Enemy(enemies_speed, enemy_movement))

    # Explosions
    explosions = []
    explosion_sound = pygame.mixer.Sound(setup.resource_path('sounds/musket-explosion-6383.wav'))

    # Sounds
    pygame.mixer.music.load(setup.resource_path('sounds/coconut.wav'))
    pygame.mixer.music.play(-1)

    while running:
        #######################################################
        # Game control
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play_again = False
                running = False   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up_held = True
                if event.key == pygame.K_DOWN:
                    down_held = True
                if event.key == pygame.K_LCTRL:
                    if not fire_held:
                        fire_away = True
                    fire_held = True
                if event.key == pygame.K_n:
                    if game_over:
                        play_again = False
                        running = False
                if event.key == pygame.K_y:
                    if game_over:
                        play_again = True
                        running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up_held = False
                if event.key == pygame.K_DOWN:
                    down_held = False
                if event.key == pygame.K_LCTRL:
                    fire_held = False

        # Collision Control
        for enemy in enemies:
            for fire in fires:
                if collide(5, fire.x, fire.y, 14, 5, enemy.x, enemy.y, 32, 24):
                    target_score += 100000
                    enemy.alive = False
                    fire.alive = False
                    for i in range(4):
                        explosions.append(ExplodingCamel(enemy.x, enemy.y, i))
                        explosion_sound.play()
            if player_alive and collide(3, PLAYER_X, player_y, 32, 24, enemy.x, enemy.y, 32, 24):
                enemy.alive = False
                player_alive = False
                for i in range(4):
                    explosions.append(ExplodingCamel(enemy.x, enemy.y, i))
                    explosions.append(ExplodingCamel(PLAYER_X, player_y, i))
                    explosion_sound.play()


        # Player movement
        if up_held and player_alive:
            player_y -= 2
            if player_y < 60:
                player_y = 60
        if down_held and player_alive:
            player_y += 2
            if player_y > 134:
                player_y = 134

        # animate player        
        player_delay += 1
        if player_delay == PLAYER_ANIMATE:
            player_delay = 0
            player_picture += 1
            if player_picture == 4:
                player_picture = 0

        # ToDo: lots of possibilities to calling through interface
        # fire
        if fire_away and len(fires) < 5 and player_alive:
            fires.append(Fire(PLAYER_X + 24, player_y + 12))
            fire_away = False
            fire_sound.play()
        for fire in fires:
            if fire.alive:
                fire.move()
            else:
                fires.remove(fire)

        # enemies
        for enemy in enemies:
            if enemy.alive:
                enemy.move()
            else:
                enemies.remove(enemy)
                target_score += 10000

        # .. add new enemies, possily higher difficulty
        enemy_increase_rate += 1
        if enemy_increase_rate >= ENEMY_INCREASE:
            enemy_increase_rate = 0
            number_of_enemies += 1
        if number_of_enemies > NUMBER_OF_ENEMIES_MAX:
            number_of_enemies = 3
            if enemy_movement == EnemyMovement.straight:
                enemy_movement = EnemyMovement.updown
            elif enemy_movement == EnemyMovement.updown:
                enemy_movement = EnemyMovement.sinus
            elif enemy_movement == EnemyMovement.sinus:
                enemy_movement = EnemyMovement.bouncing
            else:
                enemy_movement = EnemyMovement.straight
                enemies_speed += 1
        if len(enemies) < number_of_enemies:
            enemies.append(Enemy(enemies_speed, enemy_movement))

        #explosions
        for explosion in explosions:
            if explosion.alive:
                explosion.move()
            else:
                explosions.remove(explosion)

        # Score
        target_score += 100
        delta_score = target_score - score
        if player_alive:
            score += int(delta_score / 250)
        score_string = str(score)
        while len(score_string) < 10:
            score_string = '0' + score_string

        #######################################################
        # Update display
        display.Screen.blit(config.background_screen, (display.x(0), display.y(0)))

        # Mountain
        mountain_delay += 1
        if mountain_delay == MOUNTAIN_SPEED:
            mountain_delay = 0
            mountain_x += 1
            if mountain_x == 90 * 8:
                mountain_x = 0
        mountain = config.mountain_gfx.subsurface(pygame.Rect(mountain_x * display.Scale, 0, 240 * display.Scale, 72 * display.Scale)).copy()

        display.Screen.blit(mountain, (display.x(0), display.y(4)))

        # Score
        gfxlib.draw_string(10 * 8, 1, score_string, display)            

        # Explosions
        for explosion in explosions:
            draw_sprite(explosion.x, explosion.y, explosion.WIDTH, explosion.HEIGHT, config.exploding_camels[explosion.picture], display)

        # Fire
        for fire in fires:
            if fire.x < display.Width:
                draw_sprite(fire.x, fire.y, fire.WIDTH, fire.HEIGHT, config.lightning[fire.picture], display)

        # Enemies
        for enemy in enemies:
            ep = enemy.picture
            if ep == 6:
                ep = 4
            if enemy.x <= -enemy.WIDTH or not enemy.alive:
                continue
            elif enemy.x < display.Width:
                draw_sprite(enemy.x, enemy.y, enemy.WIDTH, enemy.HEIGHT, config.dromedaries[ep], display)

        # Player
        pp = player_picture
        if pp == 3:
            pp = 1
        if player_alive:
            display.Screen.blit(config.dromedaries[pp], (display.x(PLAYER_X), display.y(player_y)))
        # ToDo: remove this? Player exploding and game over appears
        elif player_dead_count > 0:
            player_dead_count -= 1
            r = int(player_dead_count / 4)
            partial_sprite = config.dromedaries[pp].subsurface(pygame.Rect(0, 0, 32 * display.Scale, r * display.Scale))
            display.Screen.blit(partial_sprite, (display.x(PLAYER_X), display.y(player_y)))
            if player_dead_count == 0:
                game_over = True

        if game_over:
            gfxlib.draw_string(10 * 8,  8 * 8, 'GAME OVER!', display)
            gfxlib.draw_string( 7 * 8, 10 * 8, 'PLAY AGAIN?  Y/N', display)    



        # Status bar

        #display.Screen.fill((i, i, i))
        pygame.display.flip()
        #print("tick " + str(clock.get_time()))
        clock.tick(60)

    # End 
    pygame.mixer.music.stop()

    return play_again

