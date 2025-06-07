import pygame

from gameobject import GameObject


class Timer(GameObject):
    def __init__(self):
        self.time = 0
        self.font = pygame.font.Font("assets/FiraCode-Regular.ttf", size=30)

    def update(self, delta):
        self.time += delta

    def draw(self, surface):
        text = self.font.render(f"{self.time:.2f}", True, (255, 255, 255))

        surface.blit(text, (50, 100))
