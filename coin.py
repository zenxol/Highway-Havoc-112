from cmu_graphics import*
from PIL import Image

class Coin:

    # Initializes constructor parameters of coin object
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        self.image = CMUImage(Image.open("images/coin.png"))
        # https://opengameart.org/content/coins-asset

    # Coin moves similar to obstacles
    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')

