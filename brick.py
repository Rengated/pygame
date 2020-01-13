from pygame import rect
from random import choices


class Brick():
    def __init__(self):
        self.rect = ""
        self.breakability = choices((True, False), weights=[9, 3])
        if self.breakability[0] == False:
            self.color = (255, 102, 102)
        elif self.breakability[0] == True:
            self.color = (214, 157, 51)
