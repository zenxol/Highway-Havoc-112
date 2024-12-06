from cmu_graphics import*
from PIL import Image

class Sign:  
    # Initializes constructor parameters for Sign class
    def __init__(self, app, x, y, speed):
        self.app = app
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.image = CMUImage(Image.open("images/sign.png"))
        # https://opengameart.org/content/road-sign-0
    # Moves similar to obstacle objects
    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')
