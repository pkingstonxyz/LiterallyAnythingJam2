"""Class for the board the tiles exist on"""
import pygame

from gameobject import GameObject


class Board(GameObject):
    def __init__(self):
        self.gridsize = int(GameObject.HEIGHT * 0.75)
        self.gridx = (GameObject.WIDTH - self.gridsize)//2
        self.gridy = (GameObject.HEIGHT - self.gridsize)//2
        self.cellsize = self.gridsize // 5.6
        self.celloffset = (self.gridsize - (self.cellsize * 5))//6
        self.grid = [[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None]]

    def check_can_move(self, fromcoords, tocoords):
        """Checks if it's possible for a tile to move from from to to"""
        fromx, fromy = fromcoords
        tox, toy = tocoords

        if tox > 4 or tox < 0 or toy > 4 or toy < 0:
            return False

        for tilex in range(fromy, toy+1):
            for tiley in range(fromx, tox+1):
                print(f"{tilex}, {tiley}")
                tile = self.grid[tiley][tilex]
                if tile:
                    return False
        return True

    def get_pixel_coords(self, x, y):
        """Returns a tuple of the top left of a cell from the board coords"""
        return (x * (self.cellsize + self.celloffset)
                + self.gridx + self.celloffset,
                y * (self.cellsize + self.celloffset)
                + self.gridy + self.celloffset)

    def update(self, delta):
        pass

    def draw(self, surface):
        # Draw iceberg
        pygame.draw.rect(surface, (200, 200, 255),
                         (self.gridx, self.gridy,
                          self.gridsize, self.gridsize))

        # Draw little outlines
        for ridx, row in enumerate(self.grid):
            for cidx, cell in enumerate(row):
                if cell:
                    cell.draw()
                else:
                    cx, cy = self.get_pixel_coords(cidx, ridx)
                    pygame.draw.rect(surface, (230, 230, 255),
                                     (cx, cy,
                                      self.cellsize, self.cellsize))
