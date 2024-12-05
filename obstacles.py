from cmu_graphics import*
from PIL import Image
# https://opengameart.org/sites/default/files/styles/thumbnail/public/YellowBuggy_strip4-4.png.png truck
# https://opengameart.org/sites/default/files/styles/medium/public/police%20car.png sedan
# https://www.andrew.cmu.edu/user/gkesden/oldscsstuff/ta/seminarabstracts/images/kosbie.jpg kosbie
class Obstacle:

    def __init__(self, app, x, y, width, height, speed):
        # Initialize obstacle properties
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        
    def move(self):
        # Move obstacle downwards
        self.y += self.speed
    
    def draw(self):
        pass

class Truck(Obstacle):
    def __init__(self, app, x, y):
        # Initialize Truck obstacle with specific dimensions and speed
        width = app.carWidth
        height = app.carHeight
        super().__init__(app, x, y, width, height, 8)
        self.image = CMUImage(Image.open("images/truckAI.png"))
        
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')

class Sedan(Obstacle):
    def __init__(self, app, x, y):
        # Initialize Sedan obstacle with specific dimensions and speed
        width = app.carWidth
        height = app.carHeight
        super().__init__(app, x, y, width, height, 10)
        self.image = CMUImage(Image.open("images/sedanAI.png"))
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')

class Kosbie(Obstacle): # Will change to more realistic object later
    def __init__(self, app, x, y):
        # Initialize Kosbie obstacle with specific dimensions and speed
        width = app.carWidth * 0.5
        height = app.carWidth * 0.5
        super().__init__(app, x, y, width, height, 20)
        self.image = CMUImage(Image.open("images/kosbieAI.jpg"))
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')


