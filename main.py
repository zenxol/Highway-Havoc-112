from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
from car import Car, RaceCar
import time
import random
from obstacles import Obstacle, Truck, Sedan, Kosbie
from explosion import Explosion
from warning import Warning 


def loadPilImage(url):
    return Image.open(urlopen(url))

def onAppStart(app):
    Obstacle.preloadImages()
    Explosion.preloadImages()
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

    app.obstacles = []
    app.lastObstacleTime = 0
    app.lastMultipleTime = 0
    app.lanePositions = [120, app.width // 2, 280]

    app.gameOn = True
    app.gameMode = None

    app.explosions = []
    app.explosionActive = True


    app.obstacleDelay = 7 # temporary change
    app.gameStartTime = time.time()

    app.warnings = []
    app.warningDuration = 1
def spawnObstacles(app):
    
    if app.gameOn:
        obstacleType = random.choice([Truck, Sedan, Kosbie])
        randomIndex = random.randint(0, 2)
        x = app.lanePositions[randomIndex]
        y = -100
        newObstacle = obstacleType(app, x, y)
        

        if not checkOverlap(newObstacle, [obs for obs, _ in app.obstacles]):
            warning = Warning(x, 60)
            currentTime = time.time()
            app.warnings.append((warning, currentTime))
            app.obstacles.append((newObstacle, currentTime))
            app.lastObstacleTime = currentTime
        

def checkOverlap(new, existing):
    for obstacle in existing:
        if isinstance(obstacle, tuple):
            obstacle = obstacle[0]
        if (abs(new.x - obstacle.x) < (new.width + obstacle.width) / 2 and
            abs(new.y - obstacle.y) < (new.height + obstacle.height) / 2):
            return True
    return False

def spawnMultipleObstacles(app):
    for _ in range(2):
        spawnObstacles(app)

def handleExplosion(app):
    if app.explosionActive:
        for explosion in app.explosions:
            explosion.update()
            if explosion.size == explosion.maxSize:
                app.car = None
                app.obstacles.clear() 
                break    
        app.explosions = [exp for exp in app.explosions if exp.isActive]
        if not app.explosions:
            app.explosionActive = False

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

    if app.car:
        app.car.draw()

    for warning, _ in app.warnings:
        warning.draw()

    for obstacle, _ in app.obstacles:
        obstacle.draw()
    
    for explosion in app.explosions:
        explosion.draw()

def onStep(app):

    if not app.gameOn:
        app.scrollSpeed = 0
        handleExplosion(app)
        return
        # app.obstacles.clear()

    if app.car != None:
        app.car.update()
    # Position of both highway images moves with scroll speed, resets once at bottom of screen
    app.highwayY += app.scrollSpeed
    if app.highwayY >= 600:
        app.highwayY = 0

    currentTime = time.time()

    for warning, spawnTime in app.warnings:
        warning.update()
    app.warnings = [(w, t) for w, t in app.warnings if currentTime - t < app.warningDuration]

    if currentTime - app.gameStartTime < app.obstacleDelay:
        return
    
    if app.gameOn:
        newObstacles = []
        for obstacle, spawnTime in app.obstacles:
            if currentTime - spawnTime >= app.warningDuration:
                obstacle.move()
            if app.car.collidesWith(obstacle) and app.car:
                app.gameOn = False
                explosion = Explosion(app, app.car.x, app.car.y)
                app.explosions.append(explosion)
                app.explosionActive = True
            if obstacle.y <= app.height:
                newObstacles.append((obstacle, spawnTime))
        app.obstacles = newObstacles

    if currentTime - app.lastObstacleTime >= 5:
        spawnObstacles(app)
        app.lastObstacleTime = currentTime
    if currentTime - app.lastMultipleTime >= 7:
        spawnObstacles(app)
        app.lastMultipleTime = currentTime

    
           
def onMousePress(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    # Car lane switches
    if app.car != None:
        if key == 'left':
            app.car.moveLeft()
        elif key == 'right':
            app.car.moveRight()

def main():
    runApp(width=400, height=600)
main()

