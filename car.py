from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Car:
    # Initallys Car class into app object, setting initially centered position and dimensions
    def __init__(self, app):
        self.app = app
        self.x = app.width // 2
        self.y = app.height - app.carHeight - 10
        self.width = app.carWidth
        self.height = app.carHeight

        # Creates list of possible X values, centered on each lane and starting (starts at middle lane)
        self.lanePositions = [120, app.width // 2, 280]
        self.laneIndex = 1
        self.x = self.lanePositions[self.laneIndex]

        # Initializes defauly car lane change variables, may adjust once more Car subclasses are createed
        self.targetLaneIndex = self.laneIndex
        self.isChangingLane = False
        self.laneChangeProgress = 0
        self.laneChangeSpeed = 0.20

    def moveLeft(self):
        # Bounds car from moving off highway, toggles changingLane behaviour
        if not self.isChangingLane and self.laneIndex > 0:
            self.targetLaneIndex = self.laneIndex - 1
            self.isChangingLane = True
            # Resets progress each time key is clicked
            self.laneChangeProgress = 0
    def moveRight(self):
        # Similar to moveLeft
        if not self.isChangingLane and self.laneIndex < 2:
            self.targetLaneIndex = self.laneIndex + 1
            self.isChangingLane = True
            self.laneChangeProgress = 0

    def update(self):
        if self.isChangingLane:
            self.laneChangeProgress += self.laneChangeSpeed
            if self.laneChangeProgress >= 1:
                self.laneChangeProgress = 1
                self.isChangingLane = False
                self.laneIndex = self.targetLaneIndex
            # Utilized perplexity.ai to implement smooth land switching (easing technique) - next 6 lines
            t = self.laneChangeProgress
            ease = t * t * (3 - 2 * t) # Smooth easing function - Cubic ease in/out

            startX = self.lanePositions[self.laneIndex]
            endX = self.lanePositions[self.targetLaneIndex]
            self.x = startX + (endX - startX) * ease # Creates easing effect, initially accelerates then deaccelerates
        
    def collidesWith(self, obstacle):
        hitboxX = self.width * 0.2
        hitboxY = self.width * 0.8
        return (abs(self.x - obstacle.x) < (hitboxX + obstacle.width) / 2 and 
                abs(self.y - obstacle.y) < (hitboxY + obstacle.height) / 2)

    def draw(self):
        pass # placeholder to be overridden by subclasses

class RaceCar(Car):
    def __init__(self, app):
        # Class inheritance since RaceCar instance is also a Car instance
        super().__init__(app)
        raceCarURL = 'https://opengameart.org/sites/default/files/styles/medium/public/RacingCar-1.png.png'
        self.image = CMUImage(loadPilImage(raceCarURL))
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')
        
