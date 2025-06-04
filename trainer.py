import random

from gameobject import GameObject


class Trainer(GameObject):
    """The trainer class that handles:
        - [x] Tile adding"""

    MIN_CAN_ADD = 1
    MAX_CAN_ADD = 3

    def __init__(self):
        self.time_since_add = 0
        print(self.time_since_add)
        self.add_threshold = random.uniform(Trainer.MIN_CAN_ADD,
                                            Trainer.MAX_CAN_ADD)
        print(self.add_threshold)

    def new_add_threshold(self):
        return random.uniform(Trainer.MIN_CAN_ADD, Trainer.MAX_CAN_ADD)

    def update(self, delta, board):
        # Add tile at set interval
        self.time_since_add += delta
        if self.time_since_add >= self.add_threshold:
            available = []
            for x in range(5):
                for y in range(5):
                    if not board.grid[y][x]:
                        available.append((x, y))

            if len(available) > 0:
                board.add_fish(random.choice(available))
            self.add_threshold = self.new_add_threshold()
            self.time_since_add = 0
