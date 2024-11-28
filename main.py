from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
from car import Car, RaceCar
import time
import random
from obstacles import Obstacle, Truck, Sedan, Kosbie
from explosion import Explosion
from warning import Warning
from coin import Coin 


def loadPilImage(url):
    return Image.open(urlopen(url))

def onAppStart(app):
    # Preload images in order to prevent lag from importing image Urls
    Obstacle.preloadImages()
    Explosion.preloadImages()
    Warning.preloadImages()
    Coin.preloadImages()
    # Image addresses are open to use from opengameart.org
    lightGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/grass_17.png'
    darkGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/tileable_grass.png'
    highwayURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Toon%20Road%20Texture.png'
    railURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Elevator%20Rail_0.png'
    coinURL = 'https://opengameart.org/sites/default/files/styles/medium/public/coin320000.png'

    # Initally background is set to one grass color, may change to checkered pattern once game is developed
    lightGrass = loadPilImage(lightGrassURL)
    darkGrass = loadPilImage(darkGrassURL)
    highway = loadPilImage(highwayURL)
    # Highway initially imported horizontally, thus rotation is needed
    highway = highway.rotate(90)
    rail = loadPilImage(railURL)
    coin = loadPilImage(coinURL)
    app.lightGrass = CMUImage(lightGrass)
    app.darkGrass = CMUImage(darkGrass)
    app.highway = CMUImage(highway)
    app.rail = CMUImage(rail)
    app.baseCoin = CMUImage(coin)
    
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
    app.scrollSpeed = 5
    # Car dimensions will be the same, regardless of instances of Car class
    app.carWidth = 110
    app.carHeight = 130
    app.car = RaceCar(app)

    # Initialize lists for obstacles, explosions, warnings, and coins
    app.obstacles = []
    app.explosions = []
    app.warnings = []
    app.coins = []

    # Set up game state variables
    app.gameScreen = None
    app.gameOn = None
    app.explosionActive = None

    # Set up timing variables for randomly generated obstacles and warning signs
    app.obstacleDelay = 5 # temporary change
    app.coinDelay = 5
    app.gameStartTime = time.time()
    app.lastObstacleTime = 0
    app.lastMultipleTime = 0
    app.warningDuration = 1
    app.lastCoinTime = 0
    app.coinSpawnInterval = 6
    # Define all three possible x lane positions
    app.lanePositions = [120, app.width // 2, 280]
    
    # Images for different screens
    startMenuImage = Image.open(r"C:\Users\zenho\OneDrive\Desktop\TERM PROJECT\startMenu.png")
    app.showStartMenu = True
    app.startMenu = CMUImage(startMenuImage)
    app.gameMode = None
    selectModeImage = Image.open(r"C:\Users\zenho\OneDrive\Desktop\TERM PROJECT\modeSelection.png")
    app.showSelectMode = False
    app.selectMode = CMUImage(selectModeImage)
    # if it is a screen, change name to ...screen for readability
    gameOverImage = Image.open(r"C:\Users\zenho\OneDrive\Desktop\TERM PROJECT\gameOver.png")
    app.gameOverScreen = CMUImage(gameOverImage)
    # Variable to prevent unintended clicks
    app.lastClickTime = 0

    # Background music and sound effects
    app.clickSfxOn = True
    app.soundtrackOn = True
    soundtrack = 'file:///C:/Users/zenho/Downloads/uZMCuXBGF1zWSljG53C9AECiD9EkgQYJ.mp3'
    app.soundtrack = Sound(soundtrack)
    app.soundtrack.play(loop=True)
    clickSfx = 'file:///C:/Users/zenho/Downloads/button-pressed-38129.mp3'
    app.clickSfx = Sound(clickSfx)    

    # Initiates variables that dynamically changes game difficulty as game progresses
    app.difficultyFactor = 1
    app.difficultyIncreaseInterval = 5
    app.lastDifficultyIncreaseTime = time.time()

    app.currentCoinCount = 0
    app.currentScoreCount = 0

    app.countdownActive = True
    app.countdownText = '3'
    app.countdownStartTime = time.time()
    app.gameStarted = False

    app.gameOver = False
    

def resetGame(app):
    app.scrollSpeed = 5
    app.difficultyFactor = 1
    app.explosions.clear()
    app.coins.clear()
    app.warnings.clear()

    app.car = RaceCar(app)
    # Set up game state variables
    app.gameScreen = True
    app.explosionActive = True

    # Set up timing variables for randomly generated obstacles and warning signs
    app.gameStartTime = time.time()
    app.lastObstacleTime = 0
    app.lastMultipleTime = 0
    app.warningDuration = 1
    app.obstacleDelay = 5

    app.currentCoinCount = 0
    app.currentScoreCount = 0

    app.countdownActive = True
    app.countdownText = '3'
    app.countdownStartTime = time.time()
    app.gameStarted = False

    app.gameOver = False

# Function to spawn obstacles
def spawnObstacles(app):
    # Randomly chooses obstacle type and lane to spawn at
    if app.gameOn:
        obstacleType = random.choice([Truck, Sedan, Kosbie])
        randomIndex = random.randint(0, 2)
        x = app.lanePositions[randomIndex]
        # Starts off screen in order to avoid overlapping with warning signs
        y = -100
        newObstacle = obstacleType(app, x, y)
        
        # Obstacles have differen speeds based on game mode
        if app.gameMode == 'Easy':
            newObstacle.speed += (app.difficultyFactor * 0.25)
        elif app.gameMode == 'Medium':
            newObstacle.speed += app.difficultyFactor
        elif app.gameMode == 'Hard':
            newObstacle.speed += (app.difficultyFactor * 1.5)
        
        # Checks for overlap, doesnt spawn if new obstacle overlaps
        if not checkOverlap(newObstacle, [obs for obs, _ in app.obstacles]):
            # Warning should have same lane positions as incoming object
            warning = Warning(x, 60)
            currentTime = time.time()
            # Adds objects to list as a tuple to track the related times (immutable)
            app.warnings.append((warning, currentTime))
            app.obstacles.append((newObstacle, currentTime))
            app.lastObstacleTime = currentTime
    
# Function to prevent obstacles from spawning on top of each other
def checkOverlap(new, existing):
    for obstacle in existing:
        # Obstacle has to be in a tuple that stores time 
        if isinstance(obstacle, tuple):
            obstacle = obstacle[0]
        # If positions of new obstacle is equal to any existing obstacle positions, then they overlap
        if (abs(new.x - obstacle.x) < (new.width + obstacle.width) / 2 and
            abs(new.y - obstacle.y) < (new.height + obstacle.height) / 2):
            return True
    return False

# Function to spawn multiple obstacles
def spawnMultipleObstacles(app):
    for _ in range(3):
        spawnObstacles(app)

# Function to handle explosions when car collides with obstacle
def handleExplosion(app):
    # ExplosionActive is initially true since explosions should occur only once
    if app.explosionActive:
        for explosion in app.explosions:
            # Update explosion animation
            explosion.update()
            # Remove all obstacles and car objects once explosion is max size
            if explosion.size == explosion.maxSize:
                app.car = None
                app.obstacles.clear()
                app.warnings.clear()
                app.coins.clear()
                app.gameOver = True
                break    
        app.explosions = [exp for exp in app.explosions if exp.isActive]
        if not app.explosions:
            app.explosionActive = False

# Function to redraw the game screen

def spawnCoin(app):
    if app.gameOn:
        randomIndex = random.randint(0, 2)
        x = app.lanePositions[randomIndex]
        y = -50
        newCoin = Coin(app, x, y)
        app.coins.append(newCoin)
    
# Function called on each step of the game
def onStep(app):
    currentTime = time.time()

    if app.countdownActive:
        handleCountdown(app, currentTime)
        return
    # Once player crashes, set game mode off and stop highway scrolling
    if not app.gameOn:
        app.scrollSpeed = 0
        handleExplosion(app)
        return
    
    if not app.gameStarted:
        app.gameStartTime = currentTime
        app.gameStarted = True

    updateGameState(app, currentTime)
    updateObstaclesAndCollisions(app, currentTime)
    updateCoins(app, currentTime)
    updateScore(app)

    

def updateGameState(app, currentTime):
    # Update player car position and lane-switching animation
    if app.car != None:
        app.car.update()
    # Position of both highway images moves with scroll speed, resets once at bottom of screen
    app.highwayY += app.scrollSpeed
    if app.highwayY >= 600:
        app.highwayY = 0

    # Increases difficulty factor and scrollspeed
    if currentTime - app.lastDifficultyIncreaseTime >= app.difficultyIncreaseInterval:
        app.difficultyFactor += 1
        app.scrollSpeed = min(80, 10 + (app.difficultyFactor * 2))
        app.obstacleDelay = max(1, app.obstacleDelay - 0.5)
        app.lastDifficultyIncreaseTime = currentTime
    # Update and remove expired warnings
    for warning, spawnTime in app.warnings:
        warning.update()
    app.warnings = [(w, t) for w, t in app.warnings if currentTime - t < app.warningDuration]

def updateObstaclesAndCollisions(app, currentTime):
    # Wait for initial obstacle delay
    if not app.gameStarted or currentTime - app.gameStartTime < app.obstacleDelay:
        return
    
    if app.gameOn:
        newObstacles = []
        for obstacle, spawnTime in app.obstacles:
            # Move obstacles once warning duration is over
            if currentTime - spawnTime >= app.warningDuration:
                obstacle.move()
            # Checks for collisons and creates explosion
            if app.car.collidesWith(obstacle) and app.car:
                app.gameOn = False
                explosion = Explosion(app.car.x, app.car.y)
                app.explosions.append(explosion)
                app.explosionActive = True
            # Obstacles are only kept when they are within game frame, once pass app.height, they disappear
            if obstacle.y <= app.height:
                newObstacles.append((obstacle, spawnTime))
        app.obstacles = newObstacles

    spawnInterval = getSpawnInterval(app)
    # Spawning at most two obstacles at the same time
    if currentTime - app.lastObstacleTime >= spawnInterval:
        spawnObstacles(app)
        app.lastObstacleTime = currentTime
    if currentTime - app.lastMultipleTime >= spawnInterval:
        spawnObstacles(app)
        app.lastMultipleTime = currentTime

def updateCoins(app, currentTime):
    if currentTime - app.gameStartTime < app.coinDelay:
        return
    if app.gameOn:
        newCoins = [] 
        for coin in app.coins:
            coin.move()
            if coin.y <= app.height:
                if app.car.collidesWith(coin):
                    app.currentCoinCount += 1
                else:
                    newCoins.append(coin)
        app.coins = newCoins
    if currentTime - app.lastCoinTime >= app.coinSpawnInterval:
        spawnCoin(app)
        app.lastCoinTime = currentTime
    
def getSpawnInterval(app):
    # Obstacle spawn interval based on game mode difficulty
    if app.gameMode == 'Easy':
        return max(2, 7 / app.difficultyFactor)
    elif app.gameMode == 'Medium':
        return max(1, 5 / app.difficultyFactor)
    elif app.gameMode == 'Hard':
        return max(0.5, 4 / app.difficultyFactor)

def updateScore(app):
    if app.gameMode == 'Easy':
        app.currentScoreCount += app.difficultyFactor * 0.25
    elif app.gameMode == 'Medium':
        app.currentScoreCount += app.difficultyFactor * 0.5
    elif app.gameMode == 'Hard':
        app.currentScoreCount += app.difficultyFactor * 0.6

def handleCountdown(app, currentTime):
    elapsedTime = currentTime - app.countdownStartTime
    if elapsedTime < 1:
        app.countdownText = '3'
    elif elapsedTime < 2:
        app.countdownText = '2'
    elif elapsedTime < 3:
        app.countdownText = '1'
    elif elapsedTime < 4:
        app.countdownText = 'GO'
    elif app.gameScreen:
        app.countdownActive = False
        app.gameOn = True
        app.gameStartTime = currentTime


# Function to handle mouse press events
# A click sound effect is played every time a button is click (clickSfx has to toggle on)          
def onMousePress(app, mouseX, mouseY):
    currentTime = time.time()
    # Avoids accidental consecutive clicks (such as unintended game mode)
    if currentTime - app.lastClickTime < 0.5:
        return
    app.lastClickTime = currentTime
    
    # Starts by playing music, toggle sound button on start menu
    if app.soundtrackOn:
        app.soundtrack.play(loop=True)
    else:
        app.soundtrack.pause()

    if app.showStartMenu:
        if 120 <= mouseX <= 280 and 200 <= mouseY <= 230:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showStartMenu = False
            # Changes screen to select game mode screen
            app.showSelectMode = True
        # Toggles music / sound effect off and on
        elif 310 <= mouseX <= 355 and 235 <= mouseY <= 290:
            app.soundtrackOn = not app.soundtrackOn
            if app.soundtrackOn:
                app.soundtrack.play(loop=True)
                if app.clickSfxOn:
                    app.clickSfx.play()
            else:
                app.soundtrack.pause()
    
    elif app.showSelectMode:
        # Sets game mode to easy
        if 60 <= mouseX <= 300 and 175 <= mouseY <= 290:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showSelectMode = False
            app.gameMode = 'Easy'
            resetGame(app)
        # Sets game mode to medium
        elif 60 <= mouseX <= 300 and 310 <= mouseY <= 410:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showSelectMode = False
            app.gameMode = 'Medium'
            resetGame(app)
        # Sets game mode to hard
        elif 60 <= mouseX <= 300 and 430 <= mouseY <= 530:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showSelectMode = False
            app.gameMode = 'Hard'
            resetGame(app)  
    if app.gameOver:
        pass

                  
# Function to handle key press events
def onKeyPress(app, key):
    # Car lane switches
    if app.car != None:
        if key == 'left':
            app.car.moveLeft()
        elif key == 'right':
            app.car.moveRight()
    if key == 'r':
        app.scrollSpeed = 0
        resetGame(app)


def redrawAll(app): 
    # Draws game screen based on what is currently true
    if app.showStartMenu:
        drawImage(app.startMenu, 0, 0, width=app.width, height=app.height)
    elif app.showSelectMode:
        drawImage(app.selectMode, 0, 0, width=app.width, height=app.height)
    elif app.gameScreen:
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
        
        if app.countdownActive:
            drawLabel(app.countdownText, 200, 300, size=150, bold=True, fill='white', border='black', borderWidth=4, font='riffic', align='center')
        
        # Draws player car if it exists
        if app.car:
            app.car.draw()
        # Draw warnings, obstacles, and explosions
        for coin in app.coins:
            coin.draw() 
        for warning, _ in app.warnings:
            warning.draw()
        for obstacle, _ in app.obstacles:
            obstacle.draw()
        for explosion in app.explosions:
            explosion.draw()  
        
        # Draw score and coin counter background/images
        drawRect(0, 0, 80, 50, fill=rgb(232, 230, 107), border='Black', borderWidth=5, opacity=75)
        drawImage(app.baseCoin, 20, 25, width=25, height=25, align='center')
        drawLabel(f'{app.currentCoinCount}', 65, 25, size=35, bold=True, fill='white', border='black', borderWidth=2, font='riffic')

        drawRect(320, 0, 80, 100, fill=rgb(232, 230, 107), border='Black', borderWidth=5, opacity=75)
        drawLabel('Score', 360, 17, size=22, bold=True, fill='white', border='black', borderWidth=2, font='riffic', align='center')
        drawLabel(rounded(app.currentScoreCount), 360, 50, size=20, bold=True, fill='white', border='black', borderWidth=1, font='riffic', align='center')

        if app.gameOver and not app.explosionActive:
            drawImage(app.gameOverScreen, 200, 350, width=350, height=450, align='center')

        

def main():
    runApp(width=400, height=600)
main()
