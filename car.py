from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Car:
    # Initalizes Car class into app object, setting initially centered position and dimensions
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
    # Function updates car animation when steering
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
        # Checks for collision between car and an obstacle
        hitboxX = self.width * 0.2
        hitboxY = self.width * 0.8
        # Hitbox values are small since distance between obstacle and lane are small 
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

class RaceCarV2(Car):
    def __init__(self, app):
        # Class inheritance since RaceCarV2 instance is also a Car instance
        super().__init__(app)
        raceCarV2URL = 'https://opengameart.org/sites/default/files/styles/medium/public/pixel_racecar_blue.png'
        self.image = CMUImage(loadPilImage(raceCarV2URL))
    
    def draw(self):
        # Dimensions change due to different picture size
        drawImage(self.image, self.x, self.y, width=self.width*1.2, height=self.height, align='center')

class SedanCar(Car):
    def __init__(self, app):
        # Class inheritance since SedanCar instance is also a Car instance
        super().__init__(app)
        sedanCarURL = 'https://opengameart.org/sites/default/files/car0.png'
        self.image = CMUImage(loadPilImage(sedanCarURL))
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width * 0.55, height=self.height * 0.7, align='center')
    
class TruckCar(Car):
    def __init__(self, app):
        # Class inheritance since TruckCar instance is also a Car instance
        super().__init__(app)
        truckCarURL = 'https://opengameart.org/sites/default/files/car-truck2_1.png'
        self.image = CMUImage(loadPilImage(truckCarURL))
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width * 0.55, height=self.height * 0.85, align='center')
