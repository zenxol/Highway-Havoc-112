from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
import time

def loadPilImage(url):
    return Image.open(urlopen(url))

class Warning:
    image = None

    @classmethod
    def preloadImages(cls):
        if cls.image == None:
            warningUrl = 'https://opengameart.org/sites/default/files/styles/thumbnail/public/warning_0.png'
            pil_image = loadPilImage(warningUrl)
            cls.image = CMUImage(pil_image)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True
        self.flashInterval = 0.2
        self.lastFlash = time.time()
        self.size = 70
        Warning.preloadImages()
    def update(self):
        currentTime = time.time()
        if currentTime - self.lastFlash > self.flashInterval:
            self.visible = not self.visible
            self.lastFlash = currentTime
    
    def draw(self):
        if self.visible:
            drawImage(Warning.image, self.x, self.y, width=self.size, height=self.size, align='center')
