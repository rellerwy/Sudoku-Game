import pygame, sys, os
pygame.init()

base_dir = os.path.abspath(os.path.dirname(__file__))

# Display
disWidth = 850
disHeight = 650
win = pygame.display.set_mode((disWidth, disHeight))
boardFile = os.path.join(base_dir, "textures", "Board.png")
board = pygame.image.load_extended(boardFile)

# Timer
clock = pygame.time.Clock()
currentTime = 0
oldTime = 0
minutes = 0
seconds = 0
timerFont = pygame.font.Font('freesansbold.ttf', 15)
timeX = 5
timeY = 630

def doTimer():
     global oldTime
     global seconds
     global minutes
     currentTime = pygame.time.get_ticks()
     if ((currentTime // 1000) > oldTime):
          if seconds + 1 >= 60:
               minutes += 1
               seconds = 0
          else:
               seconds += 1
     #print(currentTime // 1000)
     oldTime = currentTime // 1000
     clock.tick(60)

def showTimer():
     secondsTen = seconds // 10
     secondsOne = seconds - (secondsTen * 10)
     time = timerFont.render("Time: " + str(minutes) + ":" + str(secondsTen) + str(secondsOne), True, (0,0,0))
     win.blit(time, (timeX, timeY))
     
# Check Answer
buttonImgNorm = pygame.image.load(os.path.join(base_dir, "textures", "checkAnswerNorm.png"))
buttonImgPress = pygame.image.load(os.path.join(base_dir, "textures", "checkAnswerPress.png"))
buttonPixlePos = (650, 30)

isButtonPress = False
buttonArea = [650, 179 + 650, 30, 30 + 64]

def showCheckAnswer():
     if isButtonPress:
          win.blit(buttonImgPress, buttonPixlePos)
     else:
          win.blit(buttonImgNorm, buttonPixlePos)



     
# TODO: Make an object for the buttons

# Player
mousePosition = (0, 0)
squareSelectImg = pygame.image.load(os.path.join(base_dir, "textures", "selectionSquare.png"))
chooseSquareFile = os.path.join(base_dir, "textures", "doubleSelectionSquare.png")
doubleSelectImg = pygame.image.load(chooseSquareFile)

isSquareSelected = False
isSquareChosen = False
inSelect = False
squareHighlighted = (-1,-1)

def getSquare(pos):
     # Gives the grid position based on pixel measurements
     
     if pos[0] >= 5 and pos[0] <= 69:
          row = 0
     elif pos[0] >= 73 and pos[0] <= 137:
          row = 1
     elif pos[0] >= 141 and pos[0] <= 205:
          row = 2
     elif pos[0] >= 211 and pos[0] <= 275:
          row = 3
     elif pos[0] >= 279 and pos[0] <= 343:
          row = 4
     elif pos[0] >= 347 and pos[0] <= 411:
          row = 5
     elif pos[0] >= 417 and pos[0] <= 481:
          row = 6
     elif pos[0] >= 485 and pos[0] <= 549:
          row = 7
     elif pos[0] >= 553 and pos[0] <= 617:
          row = 8
     else:
          row = -1

     if pos[1] >= 5 and pos[1] <= 69:
          col = 0
     elif pos[1] >= 73 and pos[1] <= 137:
          col = 1
     elif pos[1] >= 141 and pos[1] <= 205:
          col = 2
     elif pos[1] >= 211 and pos[1] <= 275:
          col = 3
     elif pos[1] >= 279 and pos[1] <= 343:
          col = 4
     elif pos[1] >= 347 and pos[1] <= 411:
          col = 5
     elif pos[1] >= 417 and pos[1] <= 481:
          col = 6
     elif pos[1] >= 485 and pos[1] <= 549:
          col = 7
     elif pos[1] >= 553 and pos[1] <= 617:
          col = 8
     else:
          col = -1

     return (col, row)

# Pixel positions for drawing on the screen
squarePixelPositions = [[(5,5), (73, 5), (141, 5), (211, 5), (279, 5), (347, 5), (417, 5), (485, 5), (553, 5)],
                    [(5,73), (73, 73), (141, 73), (211, 73), (279, 73), (347, 73), (417, 73), (485, 73), (553, 73)],
                    [(5,141), (73, 141), (141, 141), (211, 141), (279, 141), (347, 141), (417, 141), (485, 141), (553, 141)],
                    [(5,211), (73, 211), (141, 211), (211, 211), (279, 211), (347, 211), (417, 211), (485, 211), (553, 211)],
                    [(5,279), (73, 279), (141, 279), (211, 279), (279, 279), (347, 279), (417, 279), (485, 279), (553, 279)],
                    [(5,347), (73, 347), (141, 347), (211, 347), (279, 347), (347, 347), (417, 347), (485, 347), (553, 347)],
                    [(5,417), (73, 417), (141, 417), (211, 417), (279, 417), (347, 417), (417, 417), (485, 417), (553, 417)],
                    [(5,485), (73, 485), (141, 485), (211, 485), (279, 485), (347, 485), (417, 485), (485, 485), (553, 485)],
                    [(5,553), (73, 553), (141, 553), (211, 553), (279, 553), (347, 553), (417, 553), (485, 553), (553, 553)],]

squarePixelPos = (-1,-1)


# Board Lists
# Keeps track of which square was given 
squareGiven = [[False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False]]

# Contains the number objects is there is a number, or a 0 if there is none
Board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Lists for the number objects for the notes
noteNumbers = [[[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []],
               [[], [], [], [], [], [], [], [], []]]


# Keeps track of which squares have been answered Correctly
squareAnswered = [[False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False]]

rowAnswered = [False, False, False, False, False, False, False, False, False]

columnAnswered = [False, False, False, False, False, False, False, False, False]

puzzelAnswered = False

# Drawing the square highlights
def drawSquare(pos):
     #print("Grid x:", squarePixelPos[0])
     #print("Grid y:", squarePixelPos[1])
     #print("Drawing Square")
     if pos[0] != -1 and pos[1] != -1 and not(squareGiven[pos[0]][pos[1]]):
          if isSquareChosen:
               win.blit(doubleSelectImg, squarePixelPos)
          else:
               win.blit(squareSelectImg, squarePixelPos)

# Dictionary of PNG files for the note numbers
numberDict = {'smallNumberZeros': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallNumberZeros.png')),
'smallOne': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallOne.png')),
'smallTwo': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallTwo.png')),
'smallThree': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallThree.png')),
'smallFour': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallFour.png')),
'smallFive': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallFive.png')),
'smallSix': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallSix.png')),
'smallSeven': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallSeven.png')),
'smallEight': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallEight.png')),
'smallNine': pygame.image.load(os.path.join(base_dir,'textures', 'numberTextures', 'small', 'smallNine.png'))}

numberFont = pygame.font.Font('freesansbold.ttf', 55)
filledFont = pygame.font.Font('freesansbold.ttf', 55)
filledFont.set_bold(True)

class Number(object):

     def __init__(self, numString, square, pixelPos, amNote = False):
          self.numString = numString    # The string of the number to display.
          self.square = square          # The index in the grid of the 
          self.pixelPos = pixelPos      # The position on the display to draw the image
          self.displayNumber = False    # Display this number on the screen. May not use
          self.wasGiven = False         # Was this number given by the 
          #self.amNote = amNote          # Is this number a note. May not use
          
     def drawNote(self, win):
          # This is for drawing the notes using the .png files.
          win.blit(numberDict[self.numString], (self.pixelPos[0], self.pixelPos[1]))
          #print("Number Note")

     def printNumber(self, win):
          # This is for drawing the numbers to fill in the puzzle.
          #print("Going to Print")
          if self.displayNumber == False:
               None
          else:
               if self.wasGiven:
                    # Bold black for the Given numbers
                    num = filledFont.render(self.numString, True, (0,0,0))
                    win.blit(num, (self.pixelPos[0] + 16, self.pixelPos[1] + 10))
               else:
                    # Normal and Dark Grey for the player answers
                    num = numberFont.render(self.numString, True, (80,80,80))
                    win.blit(num, (self.pixelPos[0] + 16, self.pixelPos[1] + 10))
                    #print("Was printed")

# Might Remove.
placeNumbers = [[False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False],
               [False, False, False, False, False, False, False, False, False]]

def addOrRemoveAnswer(NumString, sqr):
     # Over writes the board position 'sqr' with a new Number object of given number 'NumString'
     n = Board[sqr[0]][sqr[1]]
     if n.wasGiven == False:
          removeNoteNumberIndiscriminately(sqr)
          squareAnswered[sqr[0]][sqr[1]] = True
          n.displayNumber = True
          n.numString = NumString
          Board[sqr[0]][sqr[1]] = n
          #print("Number Added/Replaced")
     else:
          None
     
def removeAnswer(sqr):
     # Removes the Number object on board position 'sqr' and replaces it with 0
     Board[sqr[0]][sqr[1]].displayNumber = False
     squareAnswered[sqr[0]][sqr[1]] = False

def printBoard():
     # Function to draw the numbers of the board onto the screen
     for row in Board:
          for num in row:
               if num.displayNumber:
                    num.printNumber(win)
               else:
                    None

def addOrRemoveNoteNumber(NumString, sqr):
     #Haven't bothered to find the best way to do this yet, but this works fine.
     # Its 9 numbers max, who cares for efficiency. It ain't a genome sequence
     numFound = False
     for num in noteNumbers[sqr[0]][sqr[1]]:
          if num.numString == NumString:
               #print("Removing Note")
               noteNumbers[sqr[0]][sqr[1]].remove(num)
               numFound = True
               break
     if not numFound:
          #print("Adding Note")
          n = Number(NumString, sqr, squarePixelPos)
          noteNumbers[sqr[0]][sqr[1]].append(n)

def removeNoteNumberIndiscriminately(sqr):
     # Effectively removes the notes from the square 'sqr'
     noteNumbers[sqr[0]][sqr[1]] = []


# Reading a Puzzle
readNumbers = []

def readPuzzle(fileString):
     # Reads a puzzle from a text document and makes a list     
     # Makes the list of numbers to be read into
     global readNumbers
     readNumbers = []
     for r in range(9):
          readNumbers.append([])
          for c in range(9):
               readNumbers[r].append('0')

     # Read from the file
     with open(fileString) as file:
          row = 0
          col = 0
          while True:
               if row + 1 > 9:
                    row = 0
                    col += 1
               if col + 1 > 9:
                    col = 0
               char = file.read(1)
               if not char:
                    break
               if char == '\n':
                    pass
               else:
                    readNumbers[col][row] = str(char)
                    #print(char)
                    row += 1

# TODO: Make a puzzle generator

def fillOutPuzzle():
     # Takes the numbers from 'readNumbers' and adds them to the board.
     for c in range(9):
          for r in range(9):
               if readNumbers[c][r] == '0':
                    n = Number(readNumbers[c][r], (c, r), squarePixelPositions[c][r])
                    n.displayNumber = False
                    Board[c][r] = n
               else:
                    n = Number(readNumbers[c][r], (c, r), squarePixelPositions[c][r])
                    n.wasGiven = True
                    n.displayNumber = True
                    squareGiven[c][r] = True
                    Board[c][r] = n

# TODO: Finish the Puzzle Solution Verifier

def verifyPuzzleSolution():
     # Function that verifies the solution to the puzzle. I made this for testing the solution first.
     # First, verify the rule for the rows (easy)
     rowsCorrect = True
     for r in range(len(readNumbers)):
          # For each row in the puzzle,
          for n in range(len(readNumbers)):
               # we check every number in that row,
               num1 = readNumbers[r][n]
               for num2 in readNumbers[r][n+1:]:
                    # against every other number in that row
                    if num1 == num2:
                         # and if they are the same, the row is false
                         rowsCorrect = False
                         print("Row incorrect is:", r+1)
     
     # Second, verify the rule for the columns (a bit more tricky)
     columnsCorrect = True
     for c in range(len(readNumbers)):
          # For each column in the puzzle,
          for r in range(len(readNumbers)):
               # for each number in that column,
               num1 = readNumbers[r][c]
               for n in range(len(readNumbers[r+1:])):
                    # check it against every number after that in the column
                    num2 = readNumbers[r+n+1][c]
                    if num1 == num2:
                         # and if they are the same, the column is false
                         columnsCorrect = False
                         print("Column incorrect is:", c+1)
                         #print(num1, "from", c, r, "and", num2, "from", c, r+n+1)
     
     # Third, verify the rule for the squares (a lot harder)
     squaresCorrect = True
     c = 0
     d = 0
     for s in range(len(readNumbers)):
          # For each Square
          for r in range(((s//3)*3),((s//3)*3) + 3):
               # I look at the 3 rows. Here I'm saying squares go across then down.
               for n in range(c, c+3):
                    # And I look at the numbers in groups of three (the width of the square)
                    num1 = readNumbers[r][n]
                    for r2 in range(r, ((s//3)*3) + 3):
                         if r == r2:
                              d = n+1
                         else:
                              d = c
                         for n2 in range(d, c+3):
                              num2 = readNumbers[r2][n2]
                              #print("Comparing", num1, "and", num2)
                              if num1 == num2:
                                   squaresCorrect = False
                                   print("Square incorrect is", s+1)
               # Down here I scale the column range by 3 until I go over 9, then it's reset.
          c += 3
          if c >= 9:
               c = 0
     
     print("Rows Correct:", rowsCorrect)
     print("Columns Correct:", columnsCorrect)
     print("Squares Correct:", squaresCorrect)
     return rowsCorrect and columnsCorrect and squaresCorrect

def verifyPlayerAnswer():
     # Function that verifies the players answer to the puzzle
     # First, verify the rule for the rows (easy)
     rowsCorrect = True
     for r in range(len(Board)):
          # For each row in the puzzle,
          for n in range(len(Board)):
               # we check every number in that row,
               num1 = Board[r][n]
               for num2 in Board[r][n+1:]:
                    # against every other number in that row
                    if num1.numString == num2.numString:
                         # and if they are the same, the row is false
                         rowsCorrect = False
                         #print("Row incorrect is:", r+1)
     
     # Second, verify the rule for the columns (a bit more tricky)
     columnsCorrect = True
     for c in range(len(Board)):
          # For each column in the puzzle,
          for r in range(len(Board)):
               # for each number in that column,
               num1 = Board[r][c]
               for n in range(len(Board[r+1:])):
                    # check it against every number after that in the column
                    num2 = Board[r+n+1][c]
                    if num1.numString == num2.numString:
                         # and if they are the same, the column is false
                         columnsCorrect = False
                         #print("Column incorrect is:", c+1)
                         #print(num1, "from", c, r, "and", num2, "from", c, r+n+1)
     
     # Third, verify the rule for the squares (a lot harder)
     squaresCorrect = True
     c = 0
     d = 0
     for s in range(len(Board)):
          # For each Square
          for r in range(((s//3)*3),((s//3)*3) + 3):
               # I look at the 3 rows. Here I'm saying squares go across then down.
               for n in range(c, c+3):
                    # And I look at the numbers in groups of three (the width of the square)
                    num1 = Board[r][n]
                    for r2 in range(r, ((s//3)*3) + 3):
                         if r == r2:
                              d = n+1
                         else:
                              d = c
                         for n2 in range(d, c+3):
                              num2 = Board[r2][n2]
                              #print("Comparing", num1, "and", num2)
                              if num1.numString == num2.numString:
                                   squaresCorrect = False
                                   #print("Square incorrect is", s+1)
               # Down here I scale the column range by 3 until I go over 9, then it's reset.
          c += 3
          if c >= 9:
               c = 0
     
     #print("Rows Correct:", rowsCorrect)
     #print("Columns Correct:", columnsCorrect)
     #print("Squares Correct:", squaresCorrect)
     return rowsCorrect and columnsCorrect and squaresCorrect


# TODO: Show Incorrect Number's helper.

# TODO: Solves the Sudoku puzzle

# TODO: Random Sudoku puzzle generator

# For testing Porpoises
#numberOfDraws = 0

# Redrawing Game Window Function
def drawGameWindow():
     win.fill((255, 255, 255))     # Fill with white
     win.blit(board, (0,0))        # Draw Board
     
     printBoard()                  # Print the numbers on the Board
     
     # Loops to draw the notes on the board
     for i in noteNumbers:
          for j in i:
               for k in j:
                    k.drawNote(win)
     
     # Draws the highlight
     if isSquareSelected or isSquareChosen:  
          drawSquare(squareHighlighted)
     
     showCheckAnswer()
     
     showTimer()              # Draw the Timer   
     pygame.display.update()  # Update the display

     # For testing Porpoises
     #global numberOfDraws
     #numberOfDraws += 1


# Main Game Loop

#print(readNumbers)
testPuzzle = os.path.join(base_dir, 'Puzzles', 'test.txt')  # Get the test puzzle
#testPuzzle = os.path.join(base_dir, 'Puzzles', 'testSolution.txt')  # Get the test puzzle solution
readPuzzle(testPuzzle)                                      # Read the test puzzle
fillOutPuzzle()                                             # Put the puzzle in
#print(readNumbers)

# For Testing Porpoises
#testPuzzleSolution = os.path.join(base_dir, 'Puzzles', 'testSolution.txt')
#readPuzzle(testPuzzleSolution)
#verifyPuzzleSolution()

running = True
Won = False
paused = False
drawGameWindow()
while running:
     
     mouseButtons = pygame.mouse.get_pressed()
     keys = pygame.key.get_pressed()
          
     # Events
     for event in pygame.event.get():

          #drawGameWindow()
          #print(numberOfDraws)

          # Quit game
          if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
          
          #Keyboard inputs
          if event.type == pygame.KEYDOWN:
               #print("KEY IS DOWN")
               #print(noteNumbers)
               #print(Board)

               # Pause the game
               if event.key == pygame.K_PAUSE:
                    paused = True
                    while paused:
                         if event.key == pygame.K_PAUSE:
                              paused = False
               
               if event.key == pygame.K_ESCAPE:
                    isSquareChosen = isSquareSelected = False

               if isSquareSelected and not isSquareChosen:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                         addOrRemoveNoteNumber('smallOne', squareHighlighted)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                         addOrRemoveNoteNumber('smallTwo', squareHighlighted)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                         addOrRemoveNoteNumber('smallThree', squareHighlighted)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                         addOrRemoveNoteNumber('smallFour', squareHighlighted)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                         addOrRemoveNoteNumber('smallFive', squareHighlighted)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                         addOrRemoveNoteNumber('smallSix', squareHighlighted)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                         addOrRemoveNoteNumber('smallSeven', squareHighlighted)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                         addOrRemoveNoteNumber('smallEight', squareHighlighted)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                         addOrRemoveNoteNumber('smallNine', squareHighlighted)
                    elif event.key == pygame.K_BACKSPACE:
                         removeNoteNumberIndiscriminately(squareHighlighted)
               
               if isSquareChosen:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                         addOrRemoveAnswer('1', squareHighlighted)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                         addOrRemoveAnswer('2', squareHighlighted)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                         addOrRemoveAnswer('3', squareHighlighted)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                         addOrRemoveAnswer('4', squareHighlighted)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                         addOrRemoveAnswer('5', squareHighlighted)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                         addOrRemoveAnswer('6', squareHighlighted)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                         addOrRemoveAnswer('7', squareHighlighted)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                         addOrRemoveAnswer('8', squareHighlighted)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                         addOrRemoveAnswer('9', squareHighlighted)
                    elif event.key == pygame.K_BACKSPACE:
                         removeAnswer(squareHighlighted)
     
     # Mouse and Keyboard

     if mouseButtons[0]:
          mousePosition = pygame.mouse.get_pos()
          #print(mousePosition)
          #print(mousePosition[0])
          #print(mousePosition[1])
          #print(isSquareSelected)
          #print(isSquareChosen)
          buttonArea = [650, 179 + 650, 30, 30 + 64]

          highlight = getSquare(mousePosition)
          
          if not(inSelect):

               if mousePosition[0] > buttonArea[0] and mousePosition[0] < buttonArea[1] and mousePosition[1] > buttonArea[2] and mousePosition[1] < buttonArea[3]:
                    isButtonPress = True
                    #print("PRESS ME")
                    Won = verifyPlayerAnswer()
                    print(Won)
                    if Won:
                         print("Congrats. You won!")

               # If the mouse button is not being held down, do this
               inSelect = True
               #print(highlight)
               if not (highlight == (-1,-1)):
                    #If the current highlight is not out of bounds
                    #print(squareGiven[highlight[0]][highlight[1]])
                    if not(squareGiven[highlight[0]][highlight[1]]):
                         # If this is not a square that I have been given
                         #print("Square Highlight 1:",squareHighlighted)
                         if squareHighlighted == highlight:
                              # If the square to be highlighted is the same as the currently highlight
                              #print("Square Answered?", squareAnswered[squareHighlighted[0]][squareHighlighted[1]])
                              if squareAnswered[squareHighlighted[0]][squareHighlighted[1]]:
                                   # If the highlighted square has been answered
                                   isSquareSelected = False
                                   isSquareChosen = True
                              else:
                                   # The highlighted square has not been answered
                                   if isSquareSelected:
                                        # If this is the second highlight
                                        isSquareSelected = False
                                        isSquareChosen = True
                                   else:
                                        # Else, select it
                                        isSquareSelected = True
                                        isSquareChosen = False
                         else:
                              # The highlights are not the same
                              squareHighlighted = highlight
                              if squareAnswered[squareHighlighted[0]][squareHighlighted[1]]:
                                   # If the highlighted square has been answered
                                   isSquareSelected = False
                                   isSquareChosen = True
                              else:
                                   # Else, select it
                                   isSquareSelected = True
                                   isSquareChosen = False
                    else:
                         # Else it's a square I have been given, and can not select
                         isSquareSelected = False
                         isSquareChosen = False
               else:
                    #Else, the current highlight is out of bounds
                    isSquareChosen = False
                    isSquareSelected = False
                    squareHighlighted = (-1,-1)
          
          if squareHighlighted[0] != -1 and squareHighlighted[1] != -1:
               squarePixelPos = squarePixelPositions[squareHighlighted[0]][squareHighlighted[1]]
     
     if not(mouseButtons[0]):
          inSelect = False
          isButtonPress = False

     if mouseButtons[2]:
          isSquareSelected = False
          isSquareChosen = False
     
     # Timer
     if not(Won):
          doTimer()
     
     drawGameWindow()
     
     