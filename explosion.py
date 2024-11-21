from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Explosion:
    
    @classmethod
    def preloadImages(cls):
        explosionUrl = 'https://opengameart.org/sites/default/files/styles/medium/public/explosion2_1.png'
        pil_image = loadPilImage(explosionUrl)
        return CMUImage(pil_image)

    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.size = 20
        self.opacity = 10
        self.maxSize = 250
        self.maxOpacity = 100
        self.growthRate = 20
        self.fadeRate = 2
        self.isActive = True
        self.state = 'growing'
        self.image = Explosion.preloadImages()
        

    def update(self):
        if not self.isActive:
            return
        if self.state == 'growing':
            self.size = min(self.size + self.growthRate, self.maxSize)
            self.opacity = min(self.opacity + self.growthRate, self.maxOpacity)
            if self.size >= self.maxSize:
                self.state = 'fading'
        elif self.state == 'fading':
            self.opacity = max(self.opacity - self.fadeRate, 0)
            if self.opacity <= 0:
                self.isActive = False
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.size, height=self.size, opacity=self.opacity, align='center')
        
        

