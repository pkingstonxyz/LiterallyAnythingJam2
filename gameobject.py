"""The class containing a game object"""


class GameObject:
    __GameObjectID = 0
    WIDTH = None
    HEIGHT = None

    def __init__(self):
        self.objid = GameObject.__GameObjectID
        GameObject.__GameObjectID += 1
        pass

    def update(self, delta):
        pass

    def draw(self):
        pass
