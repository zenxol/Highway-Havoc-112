from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
from car import Car, RaceCar


def loadPilImage(url):
    return Image.open(urlopen(url))

def onAppStart(app):
    # Image addresses are open to use from opengameart.org
    lightGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/grass_17.png'
    darkGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/tileable_grass.png'
    highwayURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Toon%20Road%20Texture.png'
    railURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Elevator%20Rail_0.png'

    # Initally background is set to one grass color, may change to checkered pattern once game is developed
    lightGrass = loadPilImage(lightGrassURL)
    darkGrass = loadPilImage(darkGrassURL)
    highway = loadPilImage(highwayURL)
    # Highway initially imported horizontally, thus rotation is needed
    highway = highway.rotate(90)
    rail = loadPilImage(railURL)
    app.lightGrass = CMUImage(lightGrass)
    app.darkGrass = CMUImage(darkGrass)
    app.highway = CMUImage(highway)
    app.rail = CMUImage(rail)
    
    # GrassSize is high, allowing for less images to be generated: increase in frame rates
    app.grassSize = 65
    app.railWidth = 7
    app.gameMode = True
    app.rows = app.height // app.grassSize
    app.cols = app.width // app.grassSize

    # Highway drawn from top left to bottom right
    app.highwayWidth = 330
    app.highwayY = 0
    # Initial speed of scrolling background. Will be dynamically managed later.
    app.stepsPerSecond = 100
    app.scrollSpeed = 40
    # Car dimensions will be the same, regardless of instances of Car class
    app.carWidth = 110
    app.carHeight = 130
    app.car = RaceCar(app)

def redrawAll(app):
    # Draws grass background, top to bottom, only on the left and right side of the highway
    for row in range(app.rows+1):
        y = row * app.grassSize
        drawImage(app.darkGrass, 0, y, width=app.grassSize, height=app.grassSize)
    for row in range(app.rows+1):
        y = row * app.grassSize
        drawImage(app.darkGrass, 335, y, width=app.grassSize, height=app.grassSize)

    # Adds sides of the road
    drawRect(65, 0, 15, 600, fill=rgb(191, 191, 191))
    drawRect(320, 0, 15, 600, fill=rgb(191, 191, 191))
    drawRect(60, 0, 5, 600, fill=rgb(242, 242, 242))
    drawRect(335, 0, 5, 600, fill=rgb(242, 242, 242))

    # Draws two images of the same highway to display scrolling effect
    drawImage(app.highway, 35, app.highwayY, width=app.highwayWidth, height=600)
    drawImage(app.highway, 35, app.highwayY - 590, width=app.highwayWidth, height=600)

    drawImage(app.rail, 81, 300, width=app.railWidth, height=600, align='center')
    drawImage(app.rail, 319, 300, width=app.railWidth, height=600, align='center')

    app.car.draw()

def onStep(app):
    app.car.update()
    # Position of both highway images moves with scroll speed, resets once at bottom of screen
    app.highwayY += app.scrollSpeed
    if app.highwayY >= 600:
        app.highwayY = 0
              
def onMousePress(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    # Car lane switches
    if key == 'left':
        app.car.moveLeft()
    elif key == 'right':
        app.car.moveRight()

def main():
    runApp(width=400, height=600)
main()

