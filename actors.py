from enum import Enum
import math
import random

class EnemyMovement(Enum):
    straight = 0
    updown = 1
    bouncing = 2
    sinus = 3

class Enemy:
    x = 0
    y = 0
    delay = 0
    picture = 3
    alive = True
    ANIMATE = 8
    speed = 1
    enemy_movement = EnemyMovement.straight
    sine = 90
    WIDTH = 32
    HEIGHT = 24

    MIN_Y = 60
    MAX_Y = 134


    def __init__(self, speed, enemy_movement):
        self.x = random.randrange(240, 340)
        self.y = random.randrange(self.MIN_Y, self.MAX_Y)
        self.speed = speed
        self.enemy_movement = enemy_movement        
        self.going_up = bool(random.getrandbits(1))
        if enemy_movement == EnemyMovement.bouncing:
            self.sine = 90
        if enemy_movement == EnemyMovement.sinus:
            self.sine = random.randrange(0, 180)
        self.alive = True
        

    def move(self):
        self.x -= self.speed
        if self.x < -32:
            self.alive = False
        if self.enemy_movement == EnemyMovement.updown:
            if self.going_up:
                self.y -= 1
                if self.y <= self.MIN_Y:
                    self.going_up = False
            else:
                self.y += 1
                if self.y >= self.MAX_Y:
                    self.going_up = True

        if self.enemy_movement == EnemyMovement.bouncing:
            self.sine += 3
            self.y = self.MAX_Y - abs(int(math.sin(math.radians(self.sine)) * (self.MAX_Y - self.MIN_Y) ))
            if self.sine > 360:
                self.sine -= 360

        if self.enemy_movement == EnemyMovement.sinus:
            self.sine += 3
            self.y = self.MIN_Y + int((math.sin(math.radians(self.sine)) + 1) * (self.MAX_Y - self.MIN_Y) / 2 )
            if self.sine > 360:
                self.sine -= 360

        self.delay += 1
        if self.delay == self.ANIMATE:
            self.delay = 0
            self.picture += 1
            if self.picture == 7:
                self.picture = 3


class Fire:
    WIDTH = 14
    HEIGHT = 5
    ANIMATE = 3
    x = 0
    y = 0
    delay = 0
    picture = 0
    alive = True

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def move(self):
        self.x += 4

        if self.x > 240:
            self.alive = False

        self.delay += 1
        if self.delay >= self.ANIMATE:
            self.delay = 0
            self.picture += 1
            if self.picture == 6:
                self.picture = 0


class ExplodingCamel:
    x = 0
    y = 0
    alive = True
    direction = 0
    picture = 0
    SPEED = 3
    WIDTH = 16
    HEIGHT = 16
    ANIMATE = 8
    delay = 0

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction

    def move(self):
        if self.direction == 0:
            self.y -= self.SPEED
            if self.y < -self.HEIGHT:
                self.alive = False
        elif self.direction == 1:
            self.x += self.SPEED
            if self.x > 240:
                self.alive = False
        elif self.direction == 2:
            self.y += self.SPEED
            if self.y > 200:
                self.alive = False
        elif self.direction == 3:
            self.x -= self.SPEED
            if self.x < -self.WIDTH:
                self.alive = False

        self.delay += 1
        if self.delay > self.ANIMATE:
            self.delay = 0
            self.picture += 1
            if self.picture == 8:
                self.picture = 0



