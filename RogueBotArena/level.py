import pygame
import os

class Level:
    def __init__(self):
        # Load background
        bg_path = os.path.join("assets", "Background", "Background.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (1280,720)) # to fit screen

        # Load buildings
        buildings_path = os.path.join("assets", "misc", "Buildings.png")
        self.buildings_image = pygame.image.load(buildings_path).convert_alpha()
        self.buildings_image = pygame.transform.scale(self.buildings_image, (800,600)) # Resize as needed
        self.building_position = (300,300) #osition on screen

    def update(self):
        pass  # Add dynamic level logic here if needed

    def draw(self, screen):
        screen.blit(self.background, (0, 0))                      # Draw background
        screen.blit(self.buildings_image, self.building_position)  # Draw building
