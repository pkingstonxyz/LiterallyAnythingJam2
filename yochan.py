"""Class for yo-chan"""
from enum import Enum
import pygame
from gameobject import GameObject


# IDLE -> TURNING or MOVING or GYUING or NOBITEING
# TURNING -> IDLE or MOVING
# MOVING -> IDLE
# GYUING -> IDLE
# NOBITEING -> IDLE
class YoStates(Enum):
    IDLE = 1
    TURNING = 2
    MOVING = 3
    GYUING = 4
    NOBITEING = 5


class InputActions(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    GYU = 5
    NOBITE = 6
    NONE = 7


class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


action_to_direction = {
        InputActions.MOVE_UP: Directions.UP,
        InputActions.MOVE_LEFT: Directions.LEFT,
        InputActions.MOVE_RIGHT: Directions.RIGHT,
        InputActions.MOVE_DOWN: Directions.DOWN
        }


class YoChan(GameObject):
    TURN_DURATION = 0.100  # milliseconds
    MOVE_DURATION = 0.100

    def __init__(self, board):
        board.add_yochan(self, 2, 2)
        self.gridx = 2
        self.gridy = 2
        self.pixelx, self.pixely = board.get_pixel_coords(2, 2)
        self.move_elapsed = 0

        self.state = YoStates.IDLE
        self.facing = Directions.LEFT
        self.action = InputActions.NONE

        self.turn_elapsed = 0  # in ms
        self.target_direction = Directions.LEFT


    def handle_input(self, event):
        action = self.action
        # ONLY able to take an action when idling
        if self.state != YoStates.IDLE:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                action = InputActions.MOVE_LEFT
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                action = InputActions.MOVE_RIGHT
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                action = InputActions.MOVE_UP
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                action = InputActions.MOVE_DOWN
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # LEFT CLICK
                action = InputActions.NOBITE
            elif event.button == 3:  # RIGHT CLICK
                action = InputActions.GYU
        self.action = action

    def update(self, delta, board):
        # STATE TRANSITIONS
        if self.action in action_to_direction and self.state == YoStates.IDLE:
            # Handle moving/turning logic
            target_dir = action_to_direction[self.action]
            dx, dy = target_dir.value
            tx, ty = self.gridx + dx, self.gridy + dy

            if self.facing != target_dir:
                # Turning available
                self.next_direction = target_dir
                self.time_elapsed = 0
                self.state = YoStates.TURNING
            elif board.check_can_move((tx, ty)):
                # Prepare to move
                board.move_in_grid((self.gridx, self.gridy), (tx, ty))
                self.gridx = tx
                self.gridy = ty
                self.move_origin = (self.pixelx, self.pixely)
                self.move_target = board.get_pixel_coords(tx, ty)
                self.move_elapsed = 0
                self.state = YoStates.MOVING
            else:
                # Facing the right direction but blocked
                self.state = YoStates.IDLE
                self.action = InputActions.NONE
        if self.state == YoStates.TURNING:
            self.turn_elapsed += delta

        # HANDLE DEPENDING ON STATE
        if self.state == YoStates.TURNING:
            self.turn_elapsed += delta
            if self.turn_elapsed > self.TURN_DURATION:
                self.facing = self.next_direction
                self.state = YoStates.IDLE
                self.action = InputActions.NONE

        elif self.state == YoStates.MOVING:
            self.move_elapsed += delta
            progress = min(self.move_elapsed / self.MOVE_DURATION, 1.0)
            ox, oy = self.move_origin
            tx, ty = self.move_target
            self.pixelx = ox + (tx - ox) * progress
            self.pixely = oy + (ty - oy) * progress

            if progress >= 1.0:
                self.state = YoStates.IDLE
                self.action = InputActions.NONE

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.pixelx, self.pixely, 50, 50))
        pygame.draw.rect(surface, (0, 0, 0),
                         (self.pixelx + (self.facing.value[0] * 20) + 25,
                          self.pixely + (self.facing.value[1] * 20) + 25,
                          5, 5))
