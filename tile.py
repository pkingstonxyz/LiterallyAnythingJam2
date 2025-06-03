"""The class for a tile in the game"""
from enum import Enum
import pygame
from gameobject import GameObject


class TileStates(Enum):
    STILL = 1,
    MOVING = 2,
    MERGING = 3


class Tile(GameObject):
    MOVE_DURATION = 0.100

    def __init__(self, x, y, val, board):
        self.gridx = x
        self.gridy = y

        self.pixelx, self.pixely = board.get_pixel_coords(x, y)

        self.value = val

        self.move_origin = 0
        self.move_target = 0
        self.move_elapsed = 0

        self.state = TileStates.STILL

    def move_to(self, destination, board):
        print(f"MOVING TO {destination}")
        # ASSUMES THE TILE IS IN THE RIGHT LOGICAL PLACE
        # Gate to ensure tile is still
        if self.state != TileStates.STILL:
            return

        print("Made it")
        tx, ty = destination
        self.gridx = tx
        self.gridy = ty
        self.move_origin = (self.pixelx, self.pixely)
        self.move_target = board.get_pixel_coords(tx, ty)
        self.move_elapsed = 0
        self.state = TileStates.MOVING
        pass

    def update(self, delta):
        if self.state == TileStates.MOVING:
            self.move_elapsed += delta
            progress = min(self.move_elapsed / Tile.MOVE_DURATION, 1.0)
            print(progress)
            ox, oy = self.move_origin
            tx, ty = self.move_target
            self.pixelx = ox + (tx - ox) * progress
            self.pixely = oy + (ty - oy) * progress

            if progress >= 1.0:
                self.state = TileStates.STILL
        pass

    def draw(self, surface, board):  # has to be drawn on the board
        pygame.draw.rect(surface, (150, 200, 0),
                         (self.pixelx + 10, self.pixely + 10,
                          board.cellsize - 20,
                          board.cellsize - 20))
