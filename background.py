import pygame

class Background:

    def __init__(self):
        self.time = 0
        self.framerate = 24
        self.total_frames = 120
        self.sequence = [pygame.image.load(f"assets/backgroundanimation/{i:04}.png") for i in range(1, self.total_frames+1)]

    def update(self, delta):
        self.time += delta
        self.frame = int(self.time / (1 / self.framerate)) % self.total_frames

    def draw(self, surface):
        surface.blit(self.sequence[self.frame], (0,0))
