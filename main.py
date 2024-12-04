from cmu_graphics import*
from PIL import Image
from urllib.request import urlopen
from car import Car, RaceCar, RaceCarV2, SedanCar, TruckCar
import time
import random
from obstacles import Obstacle, Truck, Sedan, Kosbie
from explosion import Explosion
from warning import Warning
from coin import Coin 
from mile import Sign


def loadPilImage(url):
    return Image.open(urlopen(url))

def onAppStart(app):
    # Preload images in order to prevent lag from importing image Urls
    Obstacle.preloadImages()
    Explosion.preloadImages()
    Warning.preloadImages()
    Coin.preloadImages()
    Sign.preloadImages()
    # Image addresses are open to use from opengameart.org
    # lightGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/grass_17.png'
    # darkGrassURL = 'https://opengameart.org/sites/default/files/styles/medium/public/tileable_grass.png'
    # waterURL = 'https://opengameart.org/sites/default/files/styles/medium/public/tex_Water_thumb.jpg'
    # highwayURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Toon%20Road%20Texture.png'
    # railURL = 'https://opengameart.org/sites/default/files/styles/medium/public/Elevator%20Rail_0.png'
    # coinURL = 'https://opengameart.org/sites/default/files/styles/medium/public/coin320000.png'

    # Initally background is set to light grass color, background is cycled every 30ish seconds

    lightGrass = Image.open("images/lightGreenGrass.png")
    darkGrass = Image.open("images/darkGreenGrass.png")
    water = Image.open("images/water.jpg")
    highway = Image.open("images/highway.png")
    # Highway initially imported horizontally, thus rotation is needed
    highway = highway.rotate(90)
    rail = Image.open("images/rail.png")
    coin = Image.open("images/coin.png")

    racecar = Image.open("images/racecar.png")
    racecarV2 = Image.open("images/racecarV2.png")
    sedan = Image.open("images/sedan.png")
    truck = Image.open("images/truck.png")
    #s = loadPilImage(coinURL)
    app.lightGrass = CMUImage(lightGrass)
    app.darkGrass = CMUImage(darkGrass)
    app.water = CMUImage(water)
    app.highway = CMUImage(highway)
    app.rail = CMUImage(rail)
    app.baseCoin = CMUImage(coin)
    
    app.racecarImage = CMUImage(racecar)
    app.racecarV2Image = CMUImage(racecarV2)
    app.sedanImage = CMUImage(sedan)
    app.truckImage = CMUImage(truck)


    
    # GrassSize is high, allowing for less images to be generated: increase in frame rates
    app.grassSize = 65
    app.waterSize = 65
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
    app.car = None

    # Initialize lists for obstacles, explosions, warnings, coins, and mile signs
    app.obstacles = []
    app.explosions = []
    app.warnings = []
    app.coins = []
    app.signs = []

    # Set up game state variables
    app.gameScreen = None # Screen of the game is visible
    app.gameOn = None # Indicate when game is in active playable state
    app.gameStarted = False # Marks initial start of game session, prevents multiplie intializations of game elements
    app.gameOver = False # Indicate once user crashes 
    app.explosionActive = None

    # Set up timing variables for randomly generated obstacles and warning signs
    app.obstacleDelay = 5 # temporary change
    app.coinDelay = 5 # delay before coins / obstacles start spawning
    app.gameStartTime = time.time()
    app.lastObstacleTime = 0
    app.lastMultipleTime = 0
    app.warningDuration = 1 
    app.lastCoinTime = 0
    app.coinSpawnInterval = 6
    # Define all three possible x lane positions
    app.lanePositions = [120, app.width // 2, 280]
    
    # Images for different screens

    #startMenuUrl = ''
    #startMenuImage = loadPilImage(startMenuUrl)
    
    startMenuImage = Image.open("images/startMenu.png")
    app.showStartMenu = True # Game starts by showing start menu 
    app.startMenu = CMUImage(startMenuImage)
    app.gameMode = None
    selectModeImage = Image.open("images/modeSelection.png")
    app.showSelectMode = False
    app.selectMode = CMUImage(selectModeImage)
    # if it is a screen, later change name to ...screen for readability
    gameOverImage = Image.open("images/gameOver.png")
    app.gameOverScreen = CMUImage(gameOverImage)
    helpImage = Image.open("images/help.png")
    app.showHelp = False
    app.help = CMUImage(helpImage)
    leaderboardImage = Image.open("images/leaderboard.png")
    app.showLeaderboard = False
    app.leaderboard = CMUImage(leaderboardImage)
    shopButtonImage = Image.open("images/shopButton.png")
    app.shopButton = CMUImage(shopButtonImage) # shopButton is always shown with start menu
    shopMenuImage = Image.open("images/shopMenu.png")
    app.showShop = False
    app.shopMenu = CMUImage(shopMenuImage)

    


    # Variable to prevent unintended clicks
    app.lastClickTime = 0

    # Background music and sound effects
    app.clickSfxOn = True
    app.soundtrackOn = True
    soundtrack = 'https://opengameart.org/sites/default/files/race.mp3'
    app.soundtrack = Sound(soundtrack)
    app.soundtrack.play(loop=True) # Initially plays soundtrack when app starts
    # setVolume()
    clickSfx = 'https://opengameart.org/sites/default/files/Toom%20Click.wav'
    app.clickSfx = Sound(clickSfx)  
    coinSfx = 'https://opengameart.org/sites/default/files/Picked%20Coin%20Echo.wav' 
    app.coinSfx = Sound(coinSfx) 
    explosionSfx = 'https://opengameart.org/sites/default/files/DeathFlash.flac'
    app.explosionSfx = Sound(explosionSfx)
    countdownSfx = 'https://opengameart.org/sites/default/files/3%202%201%20go_noise-removal_equalized.wav'
    app.countdownSfx = Sound(countdownSfx)
    engineSfx = 'file:///C:/Users/zenho/Downloads/engine.mp3'
    app.engineSfx = Sound(engineSfx) # Fix engine sfx, after resetting loop, it temporarily cuts off 

    # Initiates variables that dynamically changes game difficulty as game progresses
    app.difficultyFactor = 1
    app.difficultyIncreaseInterval = 5
    app.lastDifficultyIncreaseTime = time.time()

    # Keeps track of current number values when game starts
    app.currentCoinCount = 0
    app.currentScoreCount = 0
    app.currentMileCount = 0

    # Initializes countdown variables to tell user when to start
    app.countdownActive = True
    app.countdownText = '3'
    app.countdownStartTime = time.time()

    # Background cycle variables
    app.backgroundTypes = ['lightGrass', 'darkGrass', 'water']
    app.currentBackgroundIndex = 0
    app.lastBackgroundChangeTime = time.time()
    app.backgroundChangeInterval = 30

    # Creates a dynamic background effect
    app.backgroundY = 0
    app.backgroundScrollSpeed = app.scrollSpeed

    # Stores highest 5 scores in the leaderboard
    app.top5Scores = []

    app.carList = [RaceCar(app), RaceCarV2(app), SedanCar(app), TruckCar(app)]
    app.carListIndex = 0
    app.showCar0 = False
    app.showCar1 = False
    app.showCar2 = False
    app.showCar3 = False
    
def resetGame(app):
    # Resets game factors to default parameters
    app.scrollSpeed = 5
    app.difficultyFactor = 1

    # Makes sure all unwanted objects no longer exist before game starts
    app.explosions.clear()
    app.coins.clear()
    app.warnings.clear()
    app.signs.clear()

    # Creates car object, will change later to where user can choose what car to select
    app.car = app.carList[app.carListIndex]

    # Resets up game state variables
    app.gameScreen = True
    app.explosionActive = True
    app.gameStarted = False
    app.gameOver = False

    # Resets up timing variables for randomly generated obstacles and warning signs
    app.gameStartTime = time.time()
    app.lastObstacleTime = 0
    app.lastMultipleTime = 0
    app.warningDuration = 1
    app.obstacleDelay = 5

    # Resets all current number values to 0
    app.currentCoinCount = 0
    app.currentScoreCount = 0
    app.currentMileCount = 0

    # Reset countdown variables
    app.countdownActive = True
    app.countdownText = '3'
    app.countdownStartTime = time.time()

    # Resets background to default
    app.currentBackgroundIndex = 0
    app.lastBackgroundChangeTime = time.time()
    app.backgroundY = 0
    app.backgroundScrollSpeed = app.scrollSpeed

# Function called on each step of the game
def onStep(app):
    if app.showShop:
        pass

    currentTime = time.time()

    # Show countdown before objects can spawn/move
    if app.countdownActive:
        handleCountdown(app, currentTime)
        return
    
    # Once player crashes, set game playable to inactive and stop highway scrolling
    if not app.gameOn:
        app.scrollSpeed = 0
        app.engineSfx.pause()
        handleExplosion(app)
        return
    else:
        # Play engine audio once car appears to be moving (fix the audio later)
        app.engineSfx.play(loop=True)
    
    # Start game once countdown ends
    if not app.gameStarted:
        app.gameStartTime = currentTime
        app.gameStarted = True

    updateGameState(app, currentTime)
    updateObstaclesAndCollisions(app, currentTime)
    updateCoins(app, currentTime)
    updateScore(app)
    updateMileSign(app)

# Function creates a countdown effect, notifying the user when they can steer their car
def handleCountdown(app, currentTime):
    elapsedTime = currentTime - app.countdownStartTime
    if elapsedTime < 0.1:
        # Play countdown voice as soon as countdown starts
        app.countdownSfx.play()
    elif elapsedTime < 1: 
        app.countdownText = '3'
    elif elapsedTime < 2:
        app.countdownText = '2'
    elif elapsedTime < 3:
        app.countdownText = '1'
    elif elapsedTime < 4:
        app.countdownText = 'GO'
    elif app.gameScreen:
        # Changes to game ready variables
        app.countdownActive = False
        app.gameOn = True
        app.gameStartTime = currentTime

# Function to handle explosions when car collides with obstacle
def handleExplosion(app):
    # ExplosionActive is initially true since explosions should occur only once
    if app.explosionActive:
        for explosion in app.explosions:
            # Update explosion animation
            explosion.update()
            # Remove all objects once explosion is max size
            if explosion.size == explosion.maxSize:
                app.car = None
                app.obstacles.clear()
                app.warnings.clear()
                app.coins.clear()
                app.signs.clear()
                app.gameOver = True
                break    
        app.explosions = [exp for exp in app.explosions if exp.isActive]
        # Explosion is inactive once there are no more explosions
        if not app.explosions:
            app.explosionActive = False

# Updates state of the game: car, background, warnings, and difficulty levels
def updateGameState(app, currentTime):
    # Update player car position and lane-switching animation
    if app.car != None:
        app.car.update()
    # Position of both highway images moves with scroll speed, resets once at bottom of screen
    app.highwayY += app.scrollSpeed
    if app.highwayY >= 600:
        app.highwayY = 0
    
    app.backgroundY += app.backgroundScrollSpeed
    if app.backgroundY >= app.grassSize:
        app.backgroundY = 0

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

    if app.gameOn:
        cycleBackground(app, currentTime)

# Function cycles background every 30 seconds
def cycleBackground(app, currentTime):
    if currentTime - app.lastBackgroundChangeTime >= app.backgroundChangeInterval:
        app.currentBackgroundIndex = (app.currentBackgroundIndex + 1) % len(app.backgroundTypes)
        app.lastBackgroundChangeTime = currentTime

# Function updates obstacle spawn and collision logic and scores
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
                app.explosionSfx.play()
                # Update scores once crash is detected
                updateTop5Scores(app)
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

# Function updates the 5 highest scores to display in leaderboards
def updateTop5Scores(app):
    score = app.currentScoreCount
    # Might want to improve efficiency, it is currently O(n^2)
    if len(app.top5Scores) < 5 or score > min(app.top5Scores):
        app.top5Scores.append(score)
        # Sort scores from highest to lowest
        app.top5Scores.sort(reverse=True)
        app.top5Scores = app.top5Scores[:5]

# Function obtains spawn interval in seconds based on game mode difficulty
def getSpawnInterval(app):
    if app.gameMode == 'Easy':
        return max(2, 7 / app.difficultyFactor)
    elif app.gameMode == 'Medium':
        return max(1, 5 / app.difficultyFactor)
    elif app.gameMode == 'Hard':
        return max(0.5, 4 / app.difficultyFactor)

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
        
        # Obstacles have different speeds based on game mode
        if app.gameMode == 'Easy':
            newObstacle.speed += (app.difficultyFactor * 0.25)
        elif app.gameMode == 'Medium':
            newObstacle.speed += app.difficultyFactor
        elif app.gameMode == 'Hard':
            newObstacle.speed += (app.difficultyFactor * 1.5)
        
        # Checks for overlap, doesnt spawn if new obstacle overlaps existing obstacle
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

# Function updates coin spawn logic
def updateCoins(app, currentTime):
    # Create initial delay, similar to obstacle delay
    if currentTime - app.gameStartTime < app.coinDelay:
        return    
    if app.gameOn:
        newCoins = [] 
        for coin in app.coins:
            coin.move()
            if coin.y <= app.height:
                if app.car.collidesWith(coin):
                    app.coinSfx.play()
                    # Increases coin count each time coin is collected
                    app.currentCoinCount += 1
                else:
                    newCoins.append(coin)
        app.coins = newCoins
    # Spawns coins over a constant interval
    if currentTime - app.lastCoinTime >= app.coinSpawnInterval:
        spawnCoin(app)
        app.lastCoinTime = currentTime

# Function generates coins in random lane
def spawnCoin(app):
    if app.gameOn:
        randomIndex = random.randint(0, 2)
        x = app.lanePositions[randomIndex]
        y = -50
        newCoin = Coin(app, x, y)
        app.coins.append(newCoin)

# Function updates currentScoreCount each time new game is started   
def updateScore(app):
    # Based off difficulty, score has a multiplier
    if app.gameMode == 'Easy':
        app.currentScoreCount += app.difficultyFactor * 0.25
    elif app.gameMode == 'Medium':
        app.currentScoreCount += app.difficultyFactor * 0.5
    elif app.gameMode == 'Hard':
        app.currentScoreCount += app.difficultyFactor * 0.6

# Function updates a mile sign that appears and increases every 1000 points  
def updateMileSign(app):
    if app.gameOn:
        x = 30
        y = 0
        # Mile starts at 0
        currentMile = int(app.currentScoreCount) // 1000
        while app.currentMileCount < currentMile:
            app.currentMileCount += 1
            # Current mile sign is displayed every 1000 points is reached
            newSign = Sign(app, x, y, app.scrollSpeed / 3)
            app.signs.append(newSign)

        for sign in app.signs:
            sign.move()
            if sign.y > app.height:
                # Remove sign once off screen
                app.signs.remove(sign)

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

    # Start menu mouse logic
    if app.showStartMenu:
        if 120 <= mouseX <= 280 and 210 <= mouseY <= 250:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showStartMenu = False
            # Changes screen to select game mode screen
            app.showSelectMode = True
        elif 120 <= mouseX <= 280 and 270 <= mouseY <= 310:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showStartMenu = False
            # Changes screen to help screen
            app.showHelp = True
        elif 120 <= mouseX <= 280 and 330 <= mouseY <= 380:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showStartMenu = False
            # Changes screen to leaderboard screen
            app.showLeaderboard = True
        elif 310 <= mouseX <= 400 and 530 <= mouseY <= 600:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showStartMenu = False
            app.showShop = True
        # Toggles music / sound effect off and on
        elif 310 <= mouseX <= 355 and 235 <= mouseY <= 290:
            app.soundtrackOn = not app.soundtrackOn
            if app.soundtrackOn:
                app.soundtrack.play(loop=True)
                if app.clickSfxOn:
                    app.clickSfx.play()
                app.clickSfxOn = True
            else:
                app.clickSfxOn = False
                app.soundtrack.pause()
    # Help screen logic
    elif app.showHelp:
        if 310 <= mouseX <= 400 and 530 <= mouseY <= 600:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showHelp = False
            # Switches back to start menu
            app.showStartMenu = True
    # Leaderboard screen logic
    elif app.showLeaderboard:
        if 310 <= mouseX <= 400 and 530 <= mouseY <= 600:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showLeaderboard = False
            # Switches back to start menu
            app.showStartMenu = True

    # Select game mode screen logic, then goes to gamescreen
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
    elif app.showShop:
        if 300 <= mouseX <= 400 and 520 <= mouseY <= 600:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.showShop = False
            # Switches back to start menu
            app.showStartMenu = True



    # Game over screen logic
    elif app.gameOver:
        # Restart button logic
        if 100 <= mouseX <= 300 and 305 <= mouseY <= 345:
            if app.clickSfxOn:
                app.clickSfx.play()
            resetGame(app)
        # Home screen logic, switches back to on app start variables
        elif 100 <= mouseX <= 300 and 420 <= mouseY <= 460:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.gameScreen = None
            app.gameOn = None
            app.explosionActive = None
            app.showStartMenu = True
            app.gameMode = None
            app.gameStarted = False
            app.gameOver = False
        # Leaderboard screen logic, switches back to on app start variables
        elif 100 <= mouseX <= 300 and 355 <= mouseY <= 400:
            if app.clickSfxOn:
                app.clickSfx.play()
            app.gameScreen = None
            app.gameOn = None
            app.explosionActive = None
            app.showLeaderboard = True
            app.gameMode = None
            app.gameStarted = False
            app.gameOver = False
              
# Function to handle key press events
def onKeyPress(app, key):
    # Car lane switches
    if app.car != None:
        if key == 'left':
            app.car.moveLeft()
        elif key == 'right':
            app.car.moveRight()
        elif key == 'a':
            app.car.moveLeft()
        elif key == 'd':
            app.car.moveRight()
    # User has to be playing in order to reset the game
    if key == 'r' and app.gameOn:
        app.scrollSpeed = 0
        resetGame(app)
    if key == '0' and app.showShop:
        app.showCar3 = app.showCar1 = app.showCar2 = False
        app.showCar0 = True
        app.carListIndex = 0
    elif key == '1' and app.showShop:
        app.showCar0 = app.showCar3 = app.showCar2 = False
        app.showCar1 = True
        app.carListIndex = 1
    elif key == '2' and app.showShop:
        app.showCar0 = app.showCar1 = app.showCar3 = False
        app.showCar2 = True
        app.carListIndex = 2
    elif key == '3' and app.showShop:
        app.showCar0 = app.showCar1 = app.showCar2 = False
        app.showCar3 = True
        app.carListIndex = 3

def redrawAll(app): 
    # Draws game screen based on what is currently true
    if app.showStartMenu:
        drawImage(app.startMenu, 0, 0, width=app.width, height=app.height)
        drawImage(app.shopButton, 310, 560, width=100, height=100)
    elif app.showHelp:
        drawImage(app.help, 0, 0, width=app.width, height=app.height)
    elif app.showSelectMode:
        drawImage(app.selectMode, 0, 0, width=app.width, height=app.height)
    elif app.showLeaderboard:
        drawImage(app.leaderboard, 0, 0, width=app.width, height=app.height)
        drawTop5Scores(app)
    elif app.showShop:
        drawImage(app.shopMenu, 0, 0, width=app.width, height=app.height)
        if app.showCar0:
            drawImage(app.racecarImage, 200, 200, width=app.carWidth, height=app.carHeight)
        elif app.showCar1:
            drawImage(app.racecarV2Image, 200, 200, width=app.carWidth, height=app.carHeight)
        elif app.showCar2:
            drawImage(app.sedanImage, 200, 200, width=app.carWidth, height=app.carHeight)
        elif app.showCar3:
            drawImage(app.truckImage, 200, 200, width=app.carWidth, height=app.carHeight)
        # drawImage(app.car, 200, 200, width=app.carWidth, height=app.carHeight)
    elif app.gameScreen:
        currentBackground = app.backgroundTypes[app.currentBackgroundIndex]
        # Draws background, top to bottom, only on the left and right side of the highway
        for row in range(-1, app.rows+1):
            y = row * app.grassSize + app.backgroundY
            if currentBackground == 'lightGrass':
                drawImage(app.lightGrass, 0, y, width=app.grassSize, height=app.grassSize)
                drawImage(app.lightGrass, 335, y, width=app.grassSize, height=app.grassSize)
            elif currentBackground == 'darkGrass':
                drawImage(app.darkGrass, 0, y, width=app.grassSize, height=app.grassSize)
                drawImage(app.darkGrass, 335, y, width=app.grassSize, height=app.grassSize)
            else:
                drawImage(app.water, 0, y, width=app.waterSize, height=app.waterSize)
                drawImage(app.water, 335, y, width=app.waterSize, height=app.waterSize)

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
        # Display countdown text
        if app.countdownActive:
            drawLabel(app.countdownText, 200, 300, size=150, bold=True, fill='white', border='black', borderWidth=4, font='riffic', align='center')
    
        # Draws player car if it exists
        if app.car:
            app.car.draw()
        # Draw coins, warnings, obstacles, explosions, and mile sign 
        for warning, _ in app.warnings:
            warning.draw()
        for obstacle, _ in app.obstacles:
            obstacle.draw()
        for explosion in app.explosions:
            explosion.draw() 
        for coin in app.coins:
            coin.draw()
        for sign in app.signs:
            sign.draw()
            drawLabel(app.currentMileCount, sign.x, sign.y, size=25, bold=True, fill='white', border='black', borderWidth=1, font='riffic', align='center')
        
        # Draw score and coin counter background/images
        drawRect(0, 0, 80, 50, fill=rgb(232, 230, 107), border='Black', borderWidth=5, opacity=75)
        drawImage(app.baseCoin, 20, 25, width=25, height=25, align='center')
        drawLabel(f'{app.currentCoinCount}', 65, 25, size=35, bold=True, fill='white', border='black', borderWidth=2, font='riffic')

        drawRect(320, 0, 80, 100, fill=rgb(232, 230, 107), border='Black', borderWidth=5, opacity=75)
        drawLabel('Score', 360, 17, size=22, bold=True, fill='white', border='black', borderWidth=2, font='riffic', align='center')
        drawLabel(rounded(app.currentScoreCount), 360, 50, size=20, bold=True, fill='white', border='black', borderWidth=1, font='riffic', align='center')

        # Draws game over screen once explosion animation ends
        if app.gameOver and not app.explosionActive:
            drawImage(app.gameOverScreen, 200, 350, width=350, height=450, align='center')
 
# Functions draws highest scores from top to bottom, fitting in leaderboard screen
def drawTop5Scores(app):
    for i in range(len(app.top5Scores)):
        drawLabel(rounded(app.top5Scores[i]), 140, i * 68 + 165, size=45, bold=True, border='black', borderWidth=2, fill='white', font='orbitron' ) 
    
def main():
    runApp(width=400, height=600)
main()
