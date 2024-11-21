# https://opengameart.org/sites/default/files/styles/thumbnail/public/YellowBuggy_strip4-4.png.png truck
# https://opengameart.org/sites/default/files/styles/medium/public/police%20car.png sedan
# https://www.andrew.cmu.edu/user/gkesden/oldscsstuff/ta/seminarabstracts/images/kosbie.jpg kosbie
from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen

def loadPilImage(url):
    return Image.open(urlopen(url))

class Obstacle:
    images = {}
    # Utilized perplexity.ai to set up preloadImages to reduce lag when spawning obstacle images, in preloadImages function
    @classmethod
    def preloadImages(cls):
        image_urls = {
            'Truck': 'https://opengameart.org/sites/default/files/styles/thumbnail/public/YellowBuggy_strip4-4.png.png',
            'Sedan': 'https://opengameart.org/sites/default/files/styles/medium/public/police%20car.png',
            'Kosbie': 'https://www.andrew.cmu.edu/user/gkesden/oldscsstuff/ta/seminarabstracts/images/kosbie.jpg'
        }
        for name, url, in image_urls.items():
            pil_image = loadPilImage(url)
            cls.images[name] = CMUImage(pil_image)

    def __init__(self, app, x, y, width, height, speed, imageName):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = self.images[imageName]
    def move(self):
        self.y += self.speed
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.width, height=self.height, align='center')
    
    # def collidesWith(self, other):
    #     hitboxX = self.width * 0.7
    #     hitboxY = self.height * 0.7
    #     return (abs(self.x - other.x) < (hitboxX + other.width) / 2 
    #             and abs(self.y - other.y) < (hitboxY + other.height) / 2)

class Truck(Obstacle):
    def __init__(self, app, x, y):
        width = app.carWidth
        height = app.carHeight
        super().__init__(app, x, y, width, height, 10, 'Truck')

class Sedan(Obstacle):
    def __init__(self, app, x, y):
        width = app.carWidth
        height = app.carHeight
        super().__init__(app, x, y, width, height, 10, 'Sedan')

class Kosbie(Obstacle):
    def __init__(self, app, x, y):
        width = app.carWidth * 0.5
        height = app.carWidth * 0.5
        super().__init__(app, x, y, width, height, 20, 'Kosbie')


