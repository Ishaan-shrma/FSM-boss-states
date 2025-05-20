import pygame
import os
import random

class Boss:
    def __init__(self, x, y):
        # Load the boss image from the correct path
        image_path = os.path.join("assets", "Mob", "Boar", "Idle", "Idle-Sheet.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 2
        self.health = 150
        self.state = "idle"
        self.attack_cooldown = 0
        self.projectiles = []
        self.dodge_cooldown = 0
        self.is_dodging = False
        self.dodge_duration = 20
        self.dodge_timer = 0

    def take_damage(self, amount):
        if self.is_dodging:
            print("[Boss] Dodged the attack!")
            return
        self.health -= amount
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            print("[Boss] Dead!")

    def update(self, player, dt):
        distance = player.rect.centerx - self.rect.centerx

        # Dodge randomly if player attacking
        if player.attacking and self.dodge_cooldown == 0 and not self.is_dodging:
            if random.random() < 0.3:  # 30% chance to dodge
                self.is_dodging = True
                self.dodge_timer = self.dodge_duration
                self.dodge_cooldown = 60

        if self.is_dodging:
            self.dodge_timer -= 1
            if self.dodge_timer <= 0:
                self.is_dodging = False

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= 1

        # Movement and state logic
        if abs(distance) < 300:
            if abs(distance) > 100:
                self.state = "chase"
                if distance > 0:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed
                # Add this line to update the y-position
                if player.rect.centery > self.rect.centery:
                    self.rect.y += self.speed
                else:
                    self.rect.y -= self.speed
            else:
                self.state = "attack"
        else:
            self.state = "idle"

        # Attack cooldown and logic
        if self.state == "attack":
            if self.attack_cooldown == 0:
                # Shoot projectile towards player
                proj_x = self.rect.centerx
                proj_y = self.rect.centery
                # Calculate the direction of the projectile
                dx = player.rect.centerx - proj_x
                dy = player.rect.centery - proj_y
                dist = (dx**2 + dy**2)**0.5
                if dist > 0:
                    speed_x = dx / dist * 10
                    speed_y = dy / dist * 10
                    self.projectiles.append(Projectile(proj_x, proj_y, speed_x, speed_y))
                    self.attack_cooldown = 90  # 1.5 seconds cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if proj.rect.colliderect(player.rect) and proj.active:
                player.take_damage(15)
                proj.active = False
            if not proj.active:
                self.projectiles.remove(proj)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for proj in self.projectiles:
            proj.draw(screen)

class Projectile:
    def __init__(self, x, y, speed_x, speed_y):
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.active = True

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)