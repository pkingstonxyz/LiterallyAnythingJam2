"""The class for a tile in the game"""
from enum import Enum
import pygame
from gameobject import GameObject


class TileStates(Enum):
    STILL = 1,
    MOVING = 2,
    MERGING = 3


class Tile(GameObject):
    BASE_MOVE_DURATION = 0.400
    MERGE_DURATION = 0.150

    def __init__(self, x, y, val, board):
        self.gridx = x
        self.gridy = y

        self.pixelx, self.pixely = board.get_pixel_coords(x, y)

        self.value = val

        self.move_duration = 0
        self.move_origin = 0
        self.move_target = 0
        self.move_elapsed = 0

        self.state = TileStates.STILL

        self.scale = 1.0
        self.merge_elapsed = 0
        self.has_merged_this_round = False

    def move_to(self, destination, board):
        # ASSUMES THE TILE IS IN THE RIGHT LOGICAL PLACE
        # Gate to ensure tile is still
        if self.state != TileStates.STILL and self.state != TileStates.MERGING:
            return

        tx, ty = destination
        distance = max(abs(self.gridx - tx), abs(self.gridy - ty))

        # Gate if we don't need to move
        if distance == 0:
            self.state = TileStates.STILL
            return

        self.gridx = tx
        self.gridy = ty
        self.move_origin = (self.pixelx, self.pixely)
        self.move_target = board.get_pixel_coords(tx, ty)
        self.move_elapsed = 0
        self.move_duration = (Tile.BASE_MOVE_DURATION/5) * distance
        self.state = TileStates.MOVING

    def can_merge(self, other):
        return other and self.value == other.value

    def update(self, delta):
        if self.state == TileStates.MOVING:
            self.move_elapsed += delta
            progress = min(self.move_elapsed / self.move_duration, 1.0)
            ox, oy = self.move_origin
            tx, ty = self.move_target
            self.pixelx = ox + (tx - ox) * progress
            self.pixely = oy + (ty - oy) * progress

            if progress >= 1.0:
                self.pixelx = tx
                self.pixely = ty
                self.state = TileStates.STILL

    def draw(self, surface, board):  # has to be drawn on the board
        size = int((board.cellsize - 20) * self.scale)
        offset = (board.cellsize - size) // 2
        colors = {2: (150, 200, 0),
                  4: (50, 200, 150),
                  8: (0, 150, 255),
                  16: (75, 75, 255)}
        pygame.draw.rect(surface, colors[self.value],
                         (self.pixelx + offset, self.pixely + offset,
                          size,
                          size))

    def __repr__(self):
        return f"({self.gridx},{self.gridy}):{self.value}"
