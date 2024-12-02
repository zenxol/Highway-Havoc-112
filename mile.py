from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Sign:
    image = None
    # Utilized perplexity.ai to set up preloadImages to reduce lag when spawning obstacle images, in preloadImages function
    @classmethod
    def preloadImages(cls):
        if cls.image == None:
            signUrl = 'https://opengameart.org/sites/default/files/styles/medium/public/button_6.png'
            pil_image = loadPilImage(signUrl)
            cls.image = CMUImage(pil_image)
    
    # Initializes mile object parameters
    def __init__(self, app, x, y, speed):
        self.app = app
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        Sign.preloadImages()
    
    # Moves similar to obstacle objects
    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(Sign.image, self.x, self.y, width=self.width, height=self.height, align='center')
