"""Class for yo-chan"""
from enum import Enum
import math
from directions import Directions
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


action_to_direction = {
        InputActions.MOVE_UP: Directions.UP,
        InputActions.MOVE_LEFT: Directions.LEFT,
        InputActions.MOVE_RIGHT: Directions.RIGHT,
        InputActions.MOVE_DOWN: Directions.DOWN
        }


class YoChan(GameObject):
    TURN_DURATION = (0.0166)*3    # 3 frames
    MOVE_DURATION = (0.0166)*5    # 5 frames
    NOBITE_DURATION = (0.0166)*3  # frames
    GYU_DURATION = NOBITE_DURATION

    def __init__(self, board):
        board.add_yochan(self, 2, 2)
        self.gridx = 2
        self.gridy = 2
        self.pixelx, self.pixely = board.get_pixel_coords(2, 2)
        self.move_elapsed = 0

        self.state = YoStates.NOBITEING
        self.facing = Directions.LEFT
        self.angle_direction = 0
        self.action = InputActions.NONE

        self.turn_elapsed = 0  # in ms
        self.target_direction = Directions.LEFT

        self.nobite_elapsed = 0

        self.gyu_elapsed = 0

        self.cellsize = 0
        self.animations = {
                YoStates.IDLE: {
                    1: pygame.image.load("assets/yochan/0001.png").convert_alpha(),
                    2: pygame.image.load("assets/yochan/0002.png").convert_alpha(),
                    3: pygame.image.load("assets/yochan/0003.png").convert_alpha(),
                    4: pygame.image.load("assets/yochan/0004.png").convert_alpha(),
                    5: pygame.image.load("assets/yochan/0005.png").convert_alpha(),
                    6: pygame.image.load("assets/yochan/0006.png").convert_alpha(),
                    7: pygame.image.load("assets/yochan/0007.png").convert_alpha(),
                    8: pygame.image.load("assets/yochan/0008.png").convert_alpha(),
                    9: pygame.image.load("assets/yochan/0009.png").convert_alpha(),
                    10: pygame.image.load("assets/yochan/0010.png").convert_alpha(),
                    11: pygame.image.load("assets/yochan/0011.png").convert_alpha(),
                    12: pygame.image.load("assets/yochan/0012.png").convert_alpha(),
                    }
                }

    def check_is_idling(self):
        return self.state == YoStates.IDLE

    def handle_input(self, event):
        action = self.action
        # ONLY able to take an action when idling
        if self.state != YoStates.IDLE:
            return
        leftkeys = (pygame.K_LEFT, pygame.K_a, pygame.K_h)
        rightkeys = (pygame.K_RIGHT, pygame.K_d, pygame.K_l)
        upkeys = (pygame.K_UP, pygame.K_w, pygame.K_k)
        downkeys = (pygame.K_DOWN, pygame.K_s, pygame.K_j)
        nobitekeys = (pygame.K_z, pygame.K_COMMA, pygame.K_u)
        gyukeys = (pygame.K_x, pygame.K_PERIOD, pygame.K_i)
        if event.type == pygame.KEYDOWN:
            if event.key in leftkeys:
                action = InputActions.MOVE_LEFT
            elif event.key in rightkeys:
                action = InputActions.MOVE_RIGHT
            elif event.key in upkeys:
                action = InputActions.MOVE_UP
            elif event.key in downkeys:
                action = InputActions.MOVE_DOWN
            elif event.key in nobitekeys:
                action = InputActions.NOBITE
            elif event.key in gyukeys:
                action = InputActions.GYU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            left, _, right = pygame.mouse.get_pressed()
            if left == 1:  # LEFT CLICK
                print("TRYING TO PUSH")
                action = InputActions.NOBITE
            elif right == 1:  # RIGHT CLICK
                action = InputActions.GYU
        self.action = action

    def update(self, delta, board):
        # STATE TRANSITIONS
        if self.action in action_to_direction and self.state == YoStates.IDLE:
            # Handle moving/turning logic
            target_dir = action_to_direction[self.action]
            dx, dy = target_dir.value
            tx, ty = self.gridx + dx, self.gridy + dy

            if board.check_can_move((tx, ty)):
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
        elif self.state == YoStates.IDLE and self.action == InputActions.NOBITE:
            print("I WANT TO PUSH")
            board.push_from(self.facing, (self.gridx, self.gridy))
            self.state = YoStates.NOBITEING
            self.nobite_elapsed = 0
        elif self.state == YoStates.IDLE and self.action == InputActions.GYU:
            board.pull_from(self.facing, (self.gridx, self.gridy))
            self.state = YoStates.GYUING
            self.gyu_elapsed = 0

        # Handle direction facing
        mousex, mousey = [coord * (GameObject.WIDTH / GameObject.SCREEN_WIDTH)
                          for coord in pygame.mouse.get_pos()]
        centerx = self.pixelx + board.cellsize / 2
        centery = self.pixely + board.cellsize / 2
        dx, dy = mousex - centerx, mousey - centery

        if abs(dx) > abs(dy):
            self.facing = Directions.RIGHT if dx > 0 else Directions.LEFT
        else:
            self.facing = Directions.DOWN if dy > 0 else Directions.UP

        angle_rad = math.atan2(dx, -dy)  # Swap dx and dy so that <0,1> is up
        angle_deg = math.degrees(angle_rad) % 360
        clock_pos = round(angle_deg / 30) % 12
        self.angle_direction = clock_pos
        self.cellsize = board.cellsize

        scalefactor = GameObject.WIDTH / GameObject.SCREEN_WIDTH
        mousex, mousey = pygame.mouse.get_pos()
        mousex *= scalefactor
        mousey *= scalefactor
        centerx = self.pixelx + board.cellsize / 2
        centery = self.pixely + board.cellsize / 2
        dx, dy = (mousex - centerx, mousey - centery)
        if abs(dx) > abs(dy):
            self.facing = Directions.RIGHT if dx > 0 else Directions.LEFT
        else:
            self.facing = Directions.DOWN if dy > 0 else Directions.UP

        # Handle states
        if self.state == YoStates.MOVING:
            self.move_elapsed += delta
            progress = min(self.move_elapsed / self.MOVE_DURATION, 1.0)
            ox, oy = self.move_origin
            tx, ty = self.move_target
            self.pixelx = ox + (tx - ox) * progress
            self.pixely = oy + (ty - oy) * progress

            if progress >= 1.0:
                self.state = YoStates.IDLE
                self.action = InputActions.NONE

        elif self.state == YoStates.NOBITEING:
            self.nobite_elapsed += delta
            progress = min(self.nobite_elapsed / self.NOBITE_DURATION, 1.0)
            # PUT SPRITE INTERPOLATION STUFF HERE?
            if progress >= 1.0:
                self.state = YoStates.IDLE
                self.action = InputActions.NONE

        elif self.state == YoStates.GYUING:
            self.gyu_elapsed += delta
            progress = min(self.gyu_elapsed / self.GYU_DURATION, 1.0)
            if progress >= 1.0:
                self.state = YoStates.IDLE
                self.action = InputActions.NONE

    def draw(self, surface):
        # pygame.draw.rect(surface, (0, 255, 0),
        #                 (self.pixelx, self.pixely, 50, 50))
        # pygame.draw.rect(surface, (0, 0, 0),
        #                 (self.pixelx + (self.facing.value[0] * 20) + 25,
        #                  self.pixely + (self.facing.value[1] * 20) + 25,
        #                  5, 5))
        topleftx = self.pixelx
        toplefty = self.pixely
        size = self.cellsize * 1.4
        topleftx -= size/7
        toplefty -= size/5
        if self.state == YoStates.IDLE or self.state == YoStates.MOVING:
            images = self.animations[YoStates.IDLE]
            image = images[self.angle_direction + 1]
            scaled_image = pygame.transform.scale(image, (size, size))
            surface.blit(scaled_image, (topleftx, toplefty))

    def __repr__(self):
        return "yo"
