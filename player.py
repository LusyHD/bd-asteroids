import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = 3
        self.alive = True
        self.invulnerability = False
        self.invuln_timer = (0.0)
        self.respawn_delay = (0.0)
        self.spawn_point = pygame.Vector2(x, y)
        self.flicker_timer = (0.0)

    def draw(self, screen):
        width = 2
        color = "white"

    # Show only half the time during invulnerability
        on = int(self.invuln_timer * 10) % 2 == 0  # 0.1s intervals
        if self.invulnerability and not on:
            return
        
        pygame.draw.polygon(screen, color, self.triangle(), width)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        self.wrap_position()

        if not self.alive:
            if self.lives > 0:
                self.respawn_delay -= dt
                if self.respawn_delay <= 0:
                    self.respawn()
            return

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.invulnerability:
            self.invuln_timer -= dt
            self.flicker_timer += dt
            if self.invuln_timer <= 0:
                self.invulnerability = False
        self.flicker_timer = 0.0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def wrap_position(self):
        if self.position.x < 0: self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT: self.position.y = 0

    def player_death(self):
        if not self.alive:
            return
        self.alive = False
        self.lives -= 1
        if self.lives > 0:
            self.respawn_delay = 1.0

    def respawn(self):
        self.position = self.spawn_point.copy()
        self.velocity = pygame.Vector2(0,0)
        self.angle = 0
        self.alive = True
        self.invulnerability = True
        self.invuln_timer = 2.0
