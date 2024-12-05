from cmu_graphics import*
from PIL import Image

class Sign:  
    # Initializes mile object parameters
    def __init__(self, app, x, y, speed):
        self.app = app
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.image = CMUImage(Image.open("images/sign.png"))
    
    # Moves similar to obstacle objects
    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(Sign.image, self.x, self.y, width=self.width, height=self.height, align='center')
