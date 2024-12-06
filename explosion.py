from cmu_graphics import*
from PIL import Image

class Explosion:

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
        # fadeRate is how fast the opacity decreases
        self.fadeRate = 2
        # Creates state of explosion and if it is currently occuring
        self.isActive = True
        self.state = 'growing'
        self.image = CMUImage(Image.open("images/explosion.png"))
        # https://opengameart.org/content/fiery-explosion

    # Updates explosion's size and opacity 
    def update(self):
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
        drawImage(self.image, self.x, self.y, width=self.size, height=self.size, opacity=self.opacity, align='center')
        
        

