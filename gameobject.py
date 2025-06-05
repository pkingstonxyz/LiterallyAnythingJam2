"""The class containing a game object"""


class GameObject:
    __GameObjectID = 0
    SCREEN_WIDTH = None
    WIDTH = None
    HEIGHT = None
    CELLCOUNT = 6

    def __init__(self):
        self.objid = GameObject.__GameObjectID
        GameObject.__GameObjectID += 1
        pass

    def update(self, delta):
        pass

    def draw(self):
        pass
