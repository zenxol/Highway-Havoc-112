from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Coin:
    image = None
    # Utilized perplexity.ai to set up preloadImages to reduce lag when spawning obstacle images, in preloadImages function
    @classmethod
    def preloadImages(cls):
        if cls.image == None:
            coinUrl = 'https://opengameart.org/sites/default/files/styles/medium/public/coin320000.png'
            pil_image = loadPilImage(coinUrl)
            cls.image = CMUImage(pil_image)

    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        Coin.preloadImages()

    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(Coin.image, self.x, self.y, width=self.width, height=self.height, align='center')

