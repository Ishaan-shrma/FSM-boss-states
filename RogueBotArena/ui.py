import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)
        self.player_health = 0  # Initialize player_health to 0
        self.boss_health = 0  # Initialize boss_health to 0

    def update(self, player, boss):
        self.player_health = player.health
        self.boss_health = boss.health

    def draw(self, screen):
        player_text = self.font.render(f"Player HP: {self.player_health}", True, (255, 255, 255))
        boss_text = self.font.render(f"Boss HP: {self.boss_health}", True, (255, 0, 0))

        screen.blit(player_text, (20, 20))
        screen.blit(boss_text, (20, 50))
