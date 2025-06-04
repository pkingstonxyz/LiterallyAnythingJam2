import pygame

from gameobject import GameObject

class ScoreCard(GameObject):
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, size=50)

    def score_tile(self, tile):
        self.score += tile.value

    def draw(self, surface):
        text = self.font.render(f"{self.score}", True, (255, 255, 255))
        surface.blit(text, (50, 50))

