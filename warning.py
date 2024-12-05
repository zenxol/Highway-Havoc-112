from cmu_graphics import*
from PIL import Image
import time

class Warning:

    def __init__(self, x, y):
        # Initialize warning properties
        self.x = x
        self.y = y
        self.visible = True
        self.flashInterval = 0.1 # Time between flashes in
        self.lastFlash = time.time()
        self.size = 70 
        self.image = CMUImage(Image.open("images/warning.png"))

    def update(self):
        # Update the visibility of the warning to create a flashing effect 
        currentTime = time.time()
        if currentTime - self.lastFlash > self.flashInterval:
            self.visible = not self.visible
            self.lastFlash = currentTime
    
    def draw(self):
        # Draw warning image only when visible mode is true
        if self.visible:
            drawImage(self.image, self.x, self.y, width=self.size, height=self.size, align='center')
