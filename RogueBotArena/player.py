import pygame
import os
from .player import Projectile

class Player:
    def __init__(self, x, y):
        path = os.path.join("Assets", "Character", "Idle", "Idle-Sheet.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 300  # pixels per second
        self.health = 100  # Initialize the health attribute
        self.attacking = False
        self.projectiles = []
        self.dodge_cooldown = 0
        self.is_dodging = False
        self.dodge_duration = 0.5  # seconds
        self.dodge_timer = 0

    def take_damage(self, amount):
        self.health -= amount  # Reduce the health attribute
        if self.health < 0:
            self.health = 0

    def update(self, keys, dt, boss):
        # Movement
        move_speed = self.speed * (2 if self.is_dodging else 1)
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed * dt
        if keys[pygame.K_UP]:
            self.rect.y -= move_speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += move_speed * dt
        
        # Screen boundaries
        self.rect.x = max(0, min(self.rect.x, 960 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 540 - self.rect.height))

        # Dodge mechanic
        if keys[pygame.K_d] and self.dodge_cooldown <= 0 and not self.is_dodging:
            self.is_dodging = True
            self.dodge_timer = self.dodge_duration
            self.dodge_cooldown = 1.0  # 1 second cooldown

        if self.is_dodging:
            self.dodge_timer -= dt
            if self.dodge_timer <= 0:
                self.is_dodging = False

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= dt

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update(dt)
            if not proj.active:
                self.projectiles.remove(proj)

        # Attack the boss
        if keys[pygame.K_SPACE] and not self.attacking:
            proj_x = self.rect.centerx
            proj_y = self.rect.centery
            # Calculate the direction of the projectile
            dx = boss.rect.centerx - proj_x
            dy = boss.rect.centery - proj_y
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                speed_x = dx / dist * 500
                speed_y = dy / dist * 500
                self.projectiles.append(Projectile(proj_x, proj_y, speed_x, speed_y))
                self.attacking = True

    def draw(self, screen):
        if self.is_dodging:
            temp_img = self.image.copy()
            temp_img.set_alpha(180)
            screen.blit(temp_img, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
        for proj in self.projectiles:
            proj.draw(screen)

        # Draw health bar
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = 20
        health_bar_y = 20

        health_ratio = self.health / 100
        health_bar_width = int(health_ratio * 100)
        
class Projectile:
    def __init__(self, x, y, speed_x, speed_y):
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.active = True

    def update(self, dt):
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt
        if self.rect.right < 0 or self.rect.left > 960 or self.rect.bottom < 0 or self.rect.top > 540:
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)