import pygame


class Menu:
    def __init__(self):
        self.font = pygame.font.Font("assets/FiraCode-Regular.ttf", size=40)
        pass

    def handle_input(self, event):
        pass

    def update(self, delta):
        pass

    def draw(self, surface):
        lines = ["A strange beast has invaded the seal",
                 "enclosure! Stay fed and build up to ",
                 "a 2048 tile. To enter and exit this ",
                 "menu, just press ESC. Left click to",
                 "push a block, right click to pull.",
                 "Move with WASD, Arrow keys, or HJKL.",
                 " ",
                 "THEME INTERPRETATION:",
                 "I took 2048, and spun it so that you",
                 "are playing as a lone tile. Also, it",
                 "is a mild commentary on arctic seals",
                 "being alone in a warming climate."]
        for idx, line in enumerate(lines):
            y = 50 * (idx+1)
            surface.blit(self.font.render(line, True, (255, 255, 255)), (50, y))
