import random
from enum import Enum

import pygame

from gameobject import GameObject
from directions import Directions
from yochan import YoChan


class TsukiStates(Enum):
    IDLE = 1,
    POUNCING = 2,


class Tsuki(GameObject):
    MIN_CAN_POUNCE = 3
    MAX_CAN_POUNCE = 5
    POUNCE_DURATION = 0.5

    def __init__(self):
        self.facing = None
        self.gridx = -1
        self.gridy = -1

        self.pixelx = 0
        self.pixely = 0

        self.state = TsukiStates.IDLE

        self.time_since_pounce = 0
        self.pounce_threshold = random.uniform(Tsuki.MIN_CAN_POUNCE,
                                               Tsuki.MAX_CAN_POUNCE)
        self.pounce_duration = 0
        self.pouncing_square = None
        self.original_pounce_x = None
        self.original_pounce_y = None

    def new_pounce_threshold(self):
        return random.uniform(Tsuki.MIN_CAN_POUNCE, Tsuki.MAX_CAN_POUNCE)

    def get_pouncable_squares(self, board):
        column_edges = ((0, 1), (0, 2), (0, 3), (4, 1), (4, 2), (4, 3))
        pouncable = []
        for cell in board.grid[0]:
            if cell and not isinstance(cell, YoChan):
                pouncable.append(cell)
        for cell in board.grid[4]:
            if cell and not isinstance(cell, YoChan):
                pouncable.append(cell)
        for x, y in column_edges:
            cell = board.grid[y][x]
            if cell and not isinstance(cell, YoChan):
                pouncable.append(cell)
        return pouncable

    def pounce(self, tile, board):
        board.remove_from_grid(tile)

    def update(self, delta, board):
        self.time_since_pounce += delta
        if self.time_since_pounce >= self.pounce_threshold:
            # Reset the pounce threshold and pounce timer
            self.pounce_threshold = self.new_pounce_threshold()
            self.time_since_pounce = 0
            # Check if we can actually pounce
            pounceable_squares = self.get_pouncable_squares(board)
            if len(pounceable_squares) > 0:
                self.state = TsukiStates.POUNCING
                self.pounce_duration = 0
                self.pouncing_square = random.choice(pounceable_squares)
                self.original_pounce_x = self.pouncing_square.gridx
                self.original_pounce_y = self.pouncing_square.gridy
                if self.pouncing_square.gridy == 0:
                    self.gridy = -1
                    self.gridx = self.pouncing_square.gridx
                    self.facing = Directions.DOWN
                elif self.pouncing_square.gridy == 4:
                    self.gridy = 5
                    self.gridx = self.pouncing_square.gridx
                    self.facing = Directions.UP
                elif self.pouncing_square.gridx == 0:
                    self.gridx = -1
                    self.gridy = self.pouncing_square.gridy
                    self.facing = Directions.RIGHT
                elif self.pouncing_square.gridx == 4:
                    self.gridx = 5
                    self.gridy = self.pouncing_square.gridy
                    self.facing = Directions.LEFT
                self.pixelx, self.pixely = board.get_pixel_coords(self.gridx,
                                                                  self.gridy)
            else:
                self.state = TsukiStates.IDLE

        if self.state == TsukiStates.POUNCING:
            self.pounce_duration += delta
            if self.pounce_duration >= 1.0:
                # Only pounce when tile is still there
                if (self.pouncing_square.gridx, self.pouncing_square.gridy) ==\
                        (self.original_pounce_x, self.original_pounce_y):
                    self.pounce(self.pouncing_square, board)
                self.state = TsukiStates.IDLE

    def draw(self, surface):
        # Don't draw tsuki if idling
        if self.state == TsukiStates.IDLE:
            return

        pygame.draw.rect(surface, (255, 0, 0),
                         (self.pixelx, self.pixely, 50, 50))
        pygame.draw.rect(surface, (0, 0, 0),
                         (self.pixelx + (self.facing.value[0]*20) + 25,
                          self.pixely + (self.facing.value[1]*20) + 25,
                          5, 5))
