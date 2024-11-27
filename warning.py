from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
import time

def loadPilImage(url):
    return Image.open(urlopen(url))

class Warning:
    image = None
    # Utilized perplexity.ai to set up preloadImages to reduce lag when spawning obstacle images, in preloadImages function
    @classmethod
    def preloadImages(cls):
        if cls.image == None:
            warningUrl = 'https://opengameart.org/sites/default/files/styles/thumbnail/public/warning_0.png'
            pil_image = loadPilImage(warningUrl)
            cls.image = CMUImage(pil_image)

    def __init__(self, x, y):
        # Initialize warning properties
        self.x = x
        self.y = y
        self.visible = True
        self.flashInterval = 0.1 # Time between flashes in
        self.lastFlash = time.time()
        self.size = 70 
        Warning.preloadImages()

    def update(self):
        # Update the visibility of the warning to create a flashing effect 
        currentTime = time.time()
        if currentTime - self.lastFlash > self.flashInterval:
            self.visible = not self.visible
            self.lastFlash = currentTime
    
    def draw(self):
        # Draw warning image only when visible mode is true
        if self.visible:
            drawImage(Warning.image, self.x, self.y, width=self.size, height=self.size, align='center')
