"""Class for the board the tiles exist on"""
import pygame

from gameobject import GameObject
from directions import Directions

from yochan import YoChan
from tile import Tile


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

    def check_can_move(self, tocoords):
        """Checks if it's possible for a tile to move from from to to"""
        tox, toy = tocoords

        if tox > 4 or tox < 0 or toy > 4 or toy < 0:
            return False

        return False if self.grid[toy][tox] else True

    def get_pixel_coords(self, x, y):
        """Returns a tuple of the top left of a cell from the board coords"""
        return (x * (self.cellsize + self.celloffset)
                + self.gridx + self.celloffset,
                y * (self.cellsize + self.celloffset)
                + self.gridy + self.celloffset)

    def check_if_empty(self, x, y):
        """Checks if the cell is empty(really, viable)"""
        if x > 4 or x < 0 or y > 4 or y < 0:
            return False  # not empty

        return False if self.grid[y][x] else True

    def add_yochan(self, yo, x, y):
        """Adds yo-chan to the grid"""
        self.grid[y][x] = yo

    def add_fishcube(self, x, y):
        """Adds a fishcube to the specified coordinate"""
        if self.check_if_empty(x, y):
            self.grid[y][x] = Tile(x, y, 2, self)

    def move_in_grid(self, fromcoords, tocoords):
        """updates the logical grid, does not handle any movement or tiles"""
        fromx, fromy = fromcoords
        x, y = tocoords
        if x > 4 or x < 0 or y > 4 or y < 0:
            return False
        self.grid[y][x] = self.grid[fromy][fromx]
        self.grid[fromy][fromx] = None
        return True

    def push_from(self, direction, position):
        # determine starting point for iteration
        start = 0
        step = 1
        if direction == Directions.DOWN or direction == Directions.RIGHT:
            step = -1
            start = 4

        ending_coord = position[0]
        static_coord = position[1]
        if direction == Directions.DOWN or direction == Directions.UP:
            static_coord = position[0]
            ending_coord = position[1]

        compare = lambda x, y: x < y
        if direction == Directions.UP or direction == Directions.LEFT:
            compare = lambda x, y: x > y

        # ---SLIDE---
        furthest_empty = start
        if direction == Directions.DOWN or direction == Directions.UP:
            for i in range(start, ending_coord, step):
                cell = self.grid[i][static_coord]
                if cell and compare(i, furthest_empty):
                    # If there's room to move
                    self.move_in_grid((static_coord, i),
                                      (static_coord, furthest_empty))
                    cell.move_to((static_coord, furthest_empty), self)
                    furthest_empty += step
                elif cell:
                    furthest_empty += step
        elif direction == Directions.RIGHT or direction == Directions.LEFT:
            for i in range(start, ending_coord, step):
                cell = self.grid[static_coord][i]
                if cell and compare(i, furthest_empty):
                    # If there's room to move
                    self.move_in_grid((i, static_coord),
                                      (furthest_empty, static_coord))
                    cell.move_to((furthest_empty, static_coord), self)
                    furthest_empty += step
                elif cell:
                    furthest_empty += step
        # --+MERGE+--
        if direction == Directions.DOWN or direction == Directions.UP:
            for i in range(start, ending_coord - step, step):
                cell = self.grid[i][static_coord]
                nextcell = self.grid[i+step][static_coord]
                pass
        elif direction == Directions.RIGHT or direction == Directions.LEFT:
            for i in range(start, ending_coord - step, step):
                cell = self.grid[static_coord][i]
                nextcell = self.grid[static_coord][i+step]
                pass

        print(self.grid)

    def update(self, delta):
        for row in self.grid:
            for cell in row:
                if cell and not isinstance(cell, YoChan):
                    cell.update(delta)

    def draw(self, surface):
        # Draw iceberg
        pygame.draw.rect(surface, (200, 200, 255),
                         (self.gridx, self.gridy,
                          self.gridsize, self.gridsize))

        # Draw little outlines
        for ridx, row in enumerate(self.grid):
            for cidx, cell in enumerate(row):
                cx, cy = self.get_pixel_coords(cidx, ridx)
                pygame.draw.rect(surface, (230, 230, 255),
                                 (cx, cy,
                                  self.cellsize, self.cellsize))
        # Draw actual cells
        for ridx, row in enumerate(self.grid):
            for cidx, cell in enumerate(row):
                if cell and not isinstance(cell, YoChan):
                    cell.draw(surface, self)
