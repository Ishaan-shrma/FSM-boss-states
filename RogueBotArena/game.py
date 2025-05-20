import pygame
import os
from enum import Enum, auto
from player import Player
from boss import Boss # type: ignore
from level import Level
from ui import UI

class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()
    VICTORY = auto()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.RUNNING
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        self.player = Player(100, 400)
        self.boss = Boss(700, 400)  # Using the Boss class from boss.py
        self.ui = UI()
        self.attack_cooldown = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.player.attack(self.boss)  # type: ignore # Pass the boss to the player's attack method
            self.attack_cooldown = 0.5  # 0.5 second cooldown

    def update(self, dt):
        if self.state != GameState.RUNNING:
            return
            
        keys = pygame.key.get_pressed()
        self.handle_input()
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        self.player.update(keys, dt, self.boss)  # Pass the boss to the player's update method
        self.boss.update(self.player, dt)
        self.check_collisions()
        self.check_game_state()

    def check_collisions(self):
        for proj in self.player.projectiles[:]:
            if proj.rect.colliderect(self.boss.rect): # type: ignore
                self.boss.take_damage(10)  # Use the boss's take_damage method
                self.player.projectiles.remove(proj)

    def check_game_state(self):
        if self.player.health <= 0:  # Access the health attribute of the Player class
            self.state = GameState.GAME_OVER
        elif self.boss.health <= 0:
            self.state = GameState.VICTORY

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        self.boss.draw(self.screen) # type: ignore
        self.ui.draw(self.screen)
        
        if self.state == GameState.GAME_OVER:
            self.draw_text("GAME OVER", (255, 0, 0))
        elif self.state == GameState.VICTORY:
            self.draw_text("YOU WIN!", (0, 255, 0))
        
        pygame.display.flip()

    def draw_text(self, text, color):
        font = pygame.font.SysFont(None, 72)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.update(dt)
            self.draw()