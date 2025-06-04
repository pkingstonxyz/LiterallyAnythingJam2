"""Class for the board the tiles exist on"""
import pygame

from gameobject import GameObject
from directions import Directions

from yochan import YoChan
from tile import Tile


class Board(GameObject):
    def __init__(self, scorecard):
        self.scorecard = scorecard

        self.gridsize = int(GameObject.HEIGHT * 0.75)
        self.gridx = (GameObject.WIDTH - self.gridsize)//2
        self.gridy = (GameObject.HEIGHT - self.gridsize)//2
        self.cellcount = GameObject.CELLCOUNT
        self.cellsize = self.gridsize // (self.cellcount + 0.5)
        self.celloffset = (self.gridsize - (self.cellsize * self.cellcount))//(self.cellcount+1)
        self.grid = [[None for _ in range(self.cellcount)]
                     for _ in range(self.cellcount)]

    def check_can_move(self, tocoords):
        """Checks if it's possible for a tile to move from from to to"""
        tox, toy = tocoords

        if tox > (self.cellcount-1) or tox < 0 or \
           toy > (self.cellcount-1) or toy < 0:
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
        if x > (self.cellcount-1) or x < 0 or y > (self.cellcount-1) or y < 0:
            return False  # not empty

        return False if self.grid[y][x] else True

    def add_yochan(self, yo, x, y):
        """Adds yo-chan to the grid"""
        self.grid[y][x] = yo

    def add_fish(self, coords):
        """Adds a fish to the specified coordinate"""
        x, y = coords
        if self.check_if_empty(x, y):
            self.grid[y][x] = Tile(x, y,  self)

    def in_bounds(self, x, y):
        return 0 <= x < self.cellcount and 0 <= y < self.cellcount

    def move_in_grid(self, current, target):
        print("Moving in grid")
        print(f"\tCurrent: {current}")
        print(f"\tTarget: {target}")
        cx, cy = current
        tx, ty = target
        # Gate out of bounds
        if not self.in_bounds(cx, cy) or not self.in_bounds(tx, ty):
            return False
        # Gate NOOP moves
        if (cx, cy) == (tx, ty):
            return False
        self.grid[ty][tx] = self.grid[cy][cx]
        self.grid[cy][cx] = None

    def remove_from_grid(self, tile):
        if self.in_bounds(tile.gridx, tile.gridy):
            self.grid[tile.gridy][tile.gridx] = None

    def get_affected_tiles(self, direction, position):
        x, y = position
        if direction == Directions.UP:
            if y == 0:
                return []
            tileidxes = [(x, i) for i in range(0, y)]
            pass
        elif direction == Directions.DOWN:
            if y == (self.cellcount-1):
                return []
            tileidxes = [(x, i) for i in range((self.cellcount-1), y, -1)]
        elif direction == Directions.LEFT:
            if x == 0:
                return []
            tileidxes = [(i, y) for i in range(0, x)]
            pass
        elif direction == Directions.RIGHT:
            if x == (self.cellcount-1):
                return []
            tileidxes = [(i, y) for i in range((self.cellcount-1), x, -1)]

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
        _, direction, current, _ = task
        target = self.get_target_position(current, direction)
        self.move_in_grid((current.gridx, current.gridy), target)
        if target != (current.gridx, current.gridy):
            current.move_to(target, self)
        return

    def merge_tiles(self, task):
        print("---Merging tiles---")
        _, direction, current, other = task
        print(f"\t{current} and {other}")
        print(self)
        # Get the target move
        target = self.get_target_position(current, direction)
        print(f"\tgoal: {target}")
        # Fix the logical board
        # print(self.grid)
        print(f"\tRemoving {other}")
        self.remove_from_grid(other)
        print(self)
        self.move_in_grid((current.gridx, current.gridy), target)
        print(self)
        # print(self.grid)
        # Merge the current tile up to target cell, and manage ghost cell
        print(f"\tPerforming merge up on {target}")
        current.merge_up(target, other, self)
        self.scorecard.score_tile(current)
        print(self)
        print("---Done merging---")

    def push_from(self, direction, position):
        # Gate so that we only do this if all the tiles are still
        for row in self.grid:
            for tile in row:
                if tile and not tile.check_is_idling():
                    return

        print(f"Pushing {direction} from {position}")
        tiles = self.get_affected_tiles(direction, position)
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
                # tx, ty = self.get_target_position(current, direction)
                # Check if it's able to move
                # if (tx, ty) != (current.gridx, current.gridy):
                plan.append(('move', direction, current, None))

        for task in plan:
            if task[0] == 'move':
                self.move_tile(task)
            elif task[0] == 'merge':
                self.merge_tiles(task)

    def pull_from(self, direction, position):
        # Gate so that we only do this if all the tiles are still
        for row in self.grid:
            for tile in row:
                if tile and not tile.check_is_idling():
                    return
        print(f"Pulling {direction} from {position}")
        direction_map = {
                Directions.UP: Directions.DOWN,
                Directions.DOWN: Directions.UP,
                Directions.LEFT: Directions.RIGHT,
                Directions.RIGHT: Directions.LEFT
                }
        reverse_direction = direction_map[direction]
        tiles = self.get_affected_tiles(direction, position)
        tiles = list(reversed(tiles))
        print(tiles)

        skip = False
        plan = []

        for i in range(len(tiles)):
            if skip:
                skip = False
                continue
            current = tiles[i]
            if i + 1 < len(tiles) and current.value == tiles[i+1].value:
                plan.append(('merge', reverse_direction, current, tiles[i+1]))
                skip = True  # Don't double merge
            else:
                plan.append(('move', reverse_direction, current, None))

        print(plan)

        for task in plan:
            if task[0] == 'move':
                self.move_tile(task)
            elif task[0] == 'merge':
                self.merge_tiles(task)

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

    def __repr__(self):
        return "\n".join(str(row) for row in self.grid)
