from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Explosion:
    image = None
    # Utilized perplexity.ai to set up preloadImages to reduce lag when spawning obstacle images, in preloadImages function
    @classmethod
    def preloadImages(cls):
        if cls.image == None:
            explosionUrl = 'https://opengameart.org/sites/default/files/styles/medium/public/explosion2_1.png'
            pil_image = loadPilImage(explosionUrl)
            cls.image = CMUImage(pil_image)

    def __init__(self, x, y):
        # Initialize explosion properties
        self.x = x
        self.y = y
        # Creates initial and maximum size/opacity
        self.size = 20
        self.opacity = 10
        self.maxSize = 300
        self.maxOpacity = 100
        self.growthRate = 20
        self.fadeRate = 2
        # Creates state of explosion and if it is currently occuring
        self.isActive = True
        self.state = 'growing'
        Explosion.preloadImages()
        
    def update(self):
        # Updates explosion's size and opacity 
        if not self.isActive:
            return
        if self.state == 'growing':
            # Increase size and opacity until max is reached
            self.size = min(self.size + self.growthRate, self.maxSize)
            self.opacity = min(self.opacity + self.growthRate, self.maxOpacity)
            # Once max is reached, start fading properties
            if self.size >= self.maxSize:
                self.state = 'fading'
        elif self.state == 'fading':
            # Decrease opacity untile explosion is completely faded
            self.opacity = max(self.opacity - self.fadeRate, 0)
            if self.opacity <= 0:
                self.isActive = False
    
    def draw(self):
        drawImage(Explosion.image, self.x, self.y, width=self.size, height=self.size, opacity=self.opacity, align='center')
        
        

