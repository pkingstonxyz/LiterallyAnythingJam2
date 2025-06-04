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

    def in_bounds(self, x, y):
        return 0 <= x < 5 and 0 <= y < 5

    def move_in_grid(self, current, target):
        print(f"Current: {current}")
        print(f"Target: {target}")
        cx, cy = current
        tx, ty = target
        if not self.in_bounds(cx, cy) or not self.in_bounds(tx, ty):
            return False
        self.grid[ty][tx] = self.grid[cy][cx]
        self.grid[cy][cx] = None

    def get_affected_tiles(self, direction, position):
        x, y = position
        if direction == Directions.UP:
            if y == 0:
                return []
            tileidxes = [(x, i) for i in range(0, y)]
            pass
        elif direction == Directions.DOWN:
            if y == 4:
                return []
            tileidxes = [(x, i) for i in range(4, y, -1)]
        elif direction == Directions.LEFT:
            if x == 0:
                return []
            tileidxes = [(i, y) for i in range(0, x)]
            pass
        elif direction == Directions.RIGHT:
            if x == 4:
                return []
            tileidxes = [(i, y) for i in range(4, x, -1)]

        return [self.grid[y][x] for (x, y) in tileidxes if self.grid[y][x]]


    def get_target_position(self, tile, direction):
        x, y = tile.gridx, tile.gridy
        dx, dy = direction.value

        next_x, next_y = x + dx, y + dy
        while self.in_bounds(next_x, next_y) and not self.grid[next_y][next_x]:
            x, y = next_x, next_y
            next_x += dx
            next_y += dy

        return (x, y)

    def move_tile(self, task):
        name, direction, current, target = task
        self.move_in_grid((current.gridx, current.gridy), target)
        current.move_to(target, self)
        return

    def push_from(self, direction, position):
        print(f"Pushing {direction} from {position}")
        tiles = self.get_affected_tiles(direction, position)
        for tile in tiles:
            tile.has_merged_this_round = False  # set the merging flag

        skip = False
        plan = []

        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            current = tiles[i]
            if i + 1 < len(tiles) and current.value == tiles[i+1].value:
                plan.append(('merge', direction, current, tiles[i+1]))
                skip = True  # Don't double merge
            else:
                tx, ty = self.get_target_position(current, direction)
                # Check if it's able to move
                if (tx, ty) != (current.gridx, current.gridy):
                    plan.append(('move', direction, current, (tx, ty)))

        print(plan)
        for task in plan:
            if task[0] == 'move':
                self.move_tile(task)

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
