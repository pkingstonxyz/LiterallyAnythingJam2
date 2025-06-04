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
        self.ghost_tile = None

    def check_is_idling(self):
        return self.state == TileStates.STILL

    def move_to(self, target, board):
        # ASSUMES THE TILE IS IN THE RIGHT LOGICAL PLACE
        # Gate to ensure tile is still
        if self.state != TileStates.STILL:
            return

        tx, ty = target
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

    def merge_up(self, target, other, board):
        # When merging we want to:
        # - Move self
        # - Make self have a little pop
        # - make the ghost tile scale down
        self.value *= 2
        self.state = TileStates.MERGING

        # 1. Move self
        tx, ty = target
        distance = max(abs(self.gridx - tx), abs(self.gridy - ty))

        self.gridx = tx
        self.gridy = ty
        self.move_origin = (self.pixelx, self.pixely)
        self.move_target = board.get_pixel_coords(tx, ty)
        self.move_elapsed = 0
        self.move_duration = (Tile.BASE_MOVE_DURATION/5)*distance

        # 2. Make self have a little pop
        self.scale = 1.0
        self.merge_elapsed = 0

        # 3. Make the ghost tile scale down
        otherdistance = max(abs(other.gridx - tx), abs(other.gridy - ty))
        self.ghost_tile = other
        other.gridx = tx
        other.gridy = ty
        other.move_origin = (other.pixelx, other.pixely)
        other.move_target = board.get_pixel_coords(tx, ty)
        other.move_elapsed = 0
        other.move_duration = (Tile.BASE_MOVE_DURATION/5) * otherdistance

    def can_merge(self, other):
        return other and self.value == other.value

    def scale_tween_function(self, progress):
        return progress * (-1 * progress) * (progress * 2.5) * (progress - 1)

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
        elif self.state == TileStates.MERGING:
            # When merging we want to:
            # - Move self
            # - Make self have a little pop
            # - make the ghost tile scale down while moving
            # 1. Move Self
            tx, ty = self.move_target
            if self.move_duration > 0:
                self.move_elapsed += delta
                moveprogress = min(self.move_elapsed / self.move_duration, 1.0)
                ox, oy = self.move_origin
                self.pixelx = ox + (tx - ox) * moveprogress
                self.pixely = oy + (ty - oy) * moveprogress

            # 2. Make self have a little pop
            self.merge_elapsed += delta
            mergeprogress = min(self.merge_elapsed / self.MERGE_DURATION, 1.0)
            tween = self.scale_tween_function(mergeprogress)
            self.scale = 1.0 + tween

            # 3. Make the ghost tile scale down while moving
            self.ghost_tile.scale = 1.0 - mergeprogress  # linearly scale down
            self.ghost_tile.move_elapsed += delta
            gox, goy = self.ghost_tile.move_origin
            gtx, gty = self.ghost_tile.move_target
            self.ghost_tile.pixelx = gox + (gtx - gox) * mergeprogress
            self.ghost_tile.pixely = goy + (gty - goy) * mergeprogress
            if mergeprogress >= 1.0:
                self.pixelx = tx
                self.pixely = ty
                self.ghost_tile = None
                self.scale = 1.0
                self.state = TileStates.STILL

    def draw(self, surface, board):  # has to be drawn on the board
        # If there's a ghost tile, draw it under ourselves
        if self.ghost_tile:
            self.ghost_tile.draw(surface, board)
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
