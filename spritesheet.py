import pygame

class SpriteSheet:
    
    def __init__(self, filename, dimensions, size, total_frames):
        self.frames_x, self.frames_y = dimensions
        self.frame_width, self.frame_height = size
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey((0,0,0))
        self.total_frames = total_frames

        self.frames = []

        for y in range(self.frames_y):
            for x in range(self.frames_x):
                index = y * self.frames_x + x
                if index >= total_frames:
                    return
                rect = pygame.Rect(
                    x * self.frame_width, y * self.frame_height,
                    self.frame_width, self.frame_height
                )
                image = pygame.Surface((self.frame_width, self.frame_height),
                                       pygame.SRCALPHA).convert_alpha()
                image.blit(self.sheet, (0, 0), rect)
                self.frames.append(image)

    def frame_at(self, frame_number):
        """Return the Surface of the frame at the given index."""
        if 0 <= frame_number < len(self.frames):
            return self.frames[frame_number]
        else:
            raise IndexError("Frame number out of range.")
