import pygame
pygame.init()
from random import randint
from numpy import array, swapaxes
from copy import deepcopy
from os.path import isfile
from os import listdir

class Cell:
    def __init__(self,character,fgcol=1,bgcol=0,status=0):
        self.character = character
        self.fgcol = fgcol
        self.bgcol = bgcol
        global palette, brightPalette
        self.palette = palette
        self.brightPalette = brightPalette
        self.char = None
        self.status = status

    def getCharImg(self,ignoreStatus=False):
        global chars
        if ignoreStatus:
            char = deepcopy(chars[self.character])
            for y in range(len(char)):
                for x in range(len(char[y])):
                    if char[y][x]: char[y][x] = self.palette[self.fgcol]
                    else: char[y][x] = self.palette[self.bgcol]
            char = swapaxes(array(char),0,1)
            char = pygame.surfarray.make_surface(char)
            return char
        if self.char == None:
            char = deepcopy(chars[self.character])
            for y in range(len(char)):
                for x in range(len(char[y])):
                    if self.status == 0:
                        if char[y][x]: char[y][x] = self.palette[self.fgcol]
                        else: char[y][x] = self.palette[self.bgcol]
                    elif self.status == 1:
                        if x==0 or y==0:
                            if char[y][x]: char[y][x] = self.brightPalette[self.fgcol]
                            else: char[y][x] = self.brightPalette[self.bgcol]
                        else:
                            if char[y][x]: char[y][x] = self.palette[self.fgcol]
                            else: char[y][x] = self.palette[self.bgcol]
                    elif self.status == 2:
                        if x==0 or y==0 or x==5 or y==7:
                            if char[y][x]: char[y][x] = self.brightPalette[self.fgcol]
                            else: char[y][x] = self.brightPalette[self.bgcol]
                        else:
                            if char[y][x]: char[y][x] = self.palette[self.fgcol]
                            else: char[y][x] = self.palette[self.bgcol]
            char = swapaxes(array(char),0,1)
            char = pygame.surfarray.make_surface(char)
            self.char = char
        
        return self.char

    def setFgcol(self,colour):
        self.fgcol = colour
        self.char = None

    def setBgcol(self,colour):
        self.bgcol = colour
        self.char = None

    def setChar(self,char):
        self.character = char
        self.char = None

    def setAll(self,char,fgcol,bgcol):
        self.character = char
        self.fgcol = fgcol
        self.bgcol = bgcol
        self.char = None

class TextDisplay:
    def __init__(self,width,height,myType=0):
        global screen, characterWidth, characterHeight
        self.screen = screen
        self.characterWidth = characterWidth
        self.characterHeight = characterHeight
        self.width = width
        self.height = height
        self.display = pygame.Surface((width*self.characterWidth,height*self.characterHeight))
        self.type = myType
        self.textGrid = []
        for y in range(self.height):
            toAppend = []
            for x in range(self.width):
                if self.type == 0:
                    #toAppend.append(Cell(randint(0,255)))
                    toAppend.append(Cell(32,status=1))
                elif self.type == 1: toAppend.append(Cell((y*self.width)+x))
                elif self.type == 2: toAppend.append(Cell(0,(y*self.width)+x))
            self.textGrid.append(toAppend)

    def draw(self,x,y):
        for ii in range(len(self.textGrid)):
            for i in range(len(self.textGrid[ii])):
                self.display.blit(self.textGrid[ii][i].getCharImg(), (i*self.characterWidth, ii*self.characterHeight))
        self.screen.blit(self.display,(x,y))

    def getDisplay(self):
        image = pygame.Surface((self.width*self.characterWidth,self.height*self.characterHeight))
        for ii in range(len(self.textGrid)):
            for i in range(len(self.textGrid[ii])):
                image.blit(self.textGrid[ii][i].getCharImg(True), (i*self.characterWidth, ii*self.characterHeight))
        return image

class UIText:
    def __init__(self,string,fgcol,bgcol=0):
        self.string = string
        self.fgcol = fgcol
        self.bgcol = bgcol
        self.chars = []
        global screen, characterWidth, characterHeight
        self.screen = screen
        self.characterWidth = characterWidth
        self.characterHeight = characterHeight

    def draw(self,pos):
        if self.chars == []:
            for i in self.string: self.chars.append(Cell(ord(i),self.fgcol,self.bgcol))
        for i in range(len(self.chars)):
            self.screen.blit(self.chars[i].getCharImg(), ((i+pos[0])*self.characterWidth, pos[1]*self.characterHeight))

    def setString(self,string):
        self.string = string
        self.chars = []

class UITextButton:
    def __init__(self,pos,myType,string,fgcol,bgcol=1,state=False,event=None):
        self.string = string
        self.fgcol = fgcol
        self.bgcol = bgcol
        self.chars = []
        global screen, characterWidth, characterHeight, clicks
        self.screen = screen
        self.characterWidth = characterWidth
        self.characterHeight = characterHeight
        self.state = state
        self.alreadyPressed = False
        self.type = myType
        self.pos = pos
        self.event = event
        self.clicks = clicks

    def draw(self):
        self.check()
        if self.chars == []:
            if self.state:
                for i in self.string: self.chars.append(Cell(ord(i),self.fgcol,self.bgcol))
            else:
                for i in self.string: self.chars.append(Cell(ord(i),self.bgcol,self.fgcol))
        for i in range(len(self.chars)):
            self.screen.blit(self.chars[i].getCharImg(), ((i+self.pos[0])*self.characterWidth, self.pos[1]*self.characterHeight))

    def setString(self,string):
        self.string = string
        self.chars = []

    def check(self):
        global stopInput
        mousePos = list(pygame.mouse.get_pos())
        mousePos[0] = int((mousePos[0]/self.characterWidth))
        mousePos[1] = int((mousePos[1]/self.characterHeight))
        if mousePos[0] >= self.pos[0] and mousePos[0] < self.pos[0]+len(self.string) and mousePos[1] == self.pos[1]:
            if pygame.mouse.get_pressed()[0] and (not stopInput):
                if not self.alreadyPressed:
                    self.alreadyPressed = True
                    if self.type == 0: self.state = not self.state
                    elif self.type == 1: self.state = True
                    self.chars = []
                    if self.event!=None: self.event()
                    self.clicks[int(self.state)].play()
            else:
                self.alreadyPressed = False
                if self.type == 1:
                    self.state = False
                self.chars = []
        else:
            self.alreadyPressed = False
            if self.type == 1:
                self.state = False
                self.chars = []

class UIButton:
    def __init__(self,pos,myType,fgcol,bgcol=0,state=False,event=None):
        self.type = myType
        self.fgcol = fgcol
        self.bgcol = bgcol
        self.state = state
        self.chars = [Cell(7,self.fgcol,self.bgcol),Cell(8,self.fgcol,self.bgcol)]
        global screen, characterWidth, characterHeight, clicks
        self.screen = screen
        self.characterWidth = characterWidth
        self.characterHeight = characterHeight
        self.pos = pos
        self.alreadyPressed = False
        self.event = None
        self.clicks = clicks

    def draw(self):
        self.check()
        if self.state: self.screen.blit(self.chars[0].getCharImg(), (self.pos[0]*self.characterWidth, self.pos[1]*self.characterHeight))
        else: self.screen.blit(self.chars[1].getCharImg(), (self.pos[0]*self.characterWidth, self.pos[1]*self.characterHeight))

    def check(self):
        global stopInput
        mousePos = list(pygame.mouse.get_pos())
        mousePos[0] = int((mousePos[0]/self.characterWidth))
        mousePos[1] = int((mousePos[1]/self.characterHeight))
        if mousePos[0] == self.pos[0] and mousePos[1] == self.pos[1]:
            if pygame.mouse.get_pressed()[0] and (not stopInput):
                if not self.alreadyPressed:
                    self.alreadyPressed = True
                    if self.type == 0: self.state = not self.state
                    elif self.type == 1: self.state = True
                    if self.event!=None: self.event()
                    self.clicks[int(self.state)].play()
            else:
                self.alreadyPressed = False
                if self.type == 1: self.state = False
        else:
            if pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False
                if self.type == 1: self.state = False

    def getState(self):
        return self.state

def switchColours():
    global brushSelection, brushDisplayCell
    fgcol = brushDisplayCell.fgcol
    brushDisplayCell.setFgcol(brushDisplayCell.bgcol)
    brushDisplayCell.setBgcol(fgcol)

    for y in range(len(brushSelection.textGrid)):
        for x in range(len(brushSelection.textGrid[y])):
            brushSelection.textGrid[y][x].setFgcol(brushDisplayCell.fgcol)
            brushSelection.textGrid[y][x].setBgcol(brushDisplayCell.bgcol)

def rotate(li, x):
  return li[-x % len(li):] + li[:-x % len(li)]

def shiftRight():
    global textDisplay, undoMemory, undoIndex
    for i in range(len(textDisplay.textGrid)):
        textDisplay.textGrid[i] = rotate(textDisplay.textGrid[i],1)
    undoMemory = [None,None]
    undoIndex = False

def shiftUp():
    global textDisplay, undoMemory, undoIndex
    textDisplay.textGrid = rotate(textDisplay.textGrid,-1)
    undoMemory = [None,None]
    undoIndex = False

def shiftLeft():
    global textDisplay, undoMemory, undoIndex
    for i in range(len(textDisplay.textGrid)):
        textDisplay.textGrid[i] = rotate(textDisplay.textGrid[i],-1)
    undoMemory = [None,None]
    undoIndex = False

def shiftDown():
    global textDisplay, undoMemory, undoIndex
    textDisplay.textGrid = rotate(textDisplay.textGrid,1)
    undoMemory = [None,None]
    undoIndex = False

def save():
    global textDisplay, saveVal
    textGrid = textDisplay.textGrid

    saveFile = []

    for bit in '{0:08b}'.format(len(textGrid[0])): saveFile.append(bit) # Width
    for bit in '{0:08b}'.format(len(textGrid)): saveFile.append(bit) # Height
    
    for y in textGrid:
        for x in y:
            for bit in '{0:08b}'.format(x.character): saveFile.append(bit)
            for bit in '{0:03b}'.format(x.fgcol): saveFile.append(bit)
            for bit in '{0:03b}'.format(x.bgcol): saveFile.append(bit)
            #saveFile.append(x.bgcol+(x.fgcol*16))

    #for i in range(8-(len(saveFile)%8)): saveFile.append("0")

    finalFile = []
    toAppend = []
    for i in saveFile:
        toAppend.append(i)
        if len(toAppend)==8:
            finalFile.append(int("".join(toAppend),2))
            toAppend = []

    finalFile = bytearray(finalFile)

    if saveVal == None:
        saveVal = 0
        while True:
            if not isfile("projects/project"+str(saveVal)+".bin"): break
            saveVal+=1
    if isinstance(saveVal,int):
        saveVal = "project"+str(saveVal)

    with open("projects/"+str(saveVal)+".bin", "wb") as file:
        file.write(finalFile)

    pygame.display.set_caption("TXTART - "+saveVal)

def readBits(file,number):
    bits = "".join(file[:number])
    for i in range(number): file.pop(0)
    return bits

def setUpLoad():
    global loadCheck
    loadCheck = True

def cancelLoad():
    global loadCheck
    loadCheck = False

def load(withGrid=True):
    global textDisplay, saveVal, loadCheck, undoMemory, undoIndex, titleScreen

    if withGrid:

        loadCheck = False

        with open("Which file to load.txt", "rt") as file:
            for i in range(3): file.readline()
            toLoad = file.readline()

        saveVal = toLoad

        toLoad = "projects/"+toLoad

    else:

        toLoad = "logo"

    with open(toLoad+".bin", "rb") as file:
        loadedFile = file.read()

    loadedFile = list(loadedFile)
    finalLoadedFile = []
    for i in loadedFile:
        for ii in '{0:08b}'.format(i): finalLoadedFile.append(ii)

    width = int(readBits(finalLoadedFile,8),2)
    height = int(readBits(finalLoadedFile,8),2)

    textGrid = []

    for y in range(height):
        toAppend = []
        for x in range(width):
            toAppend.append(Cell(int(readBits(finalLoadedFile,8),2),int(readBits(finalLoadedFile,3),2),int(readBits(finalLoadedFile,3),2),int(withGrid)))
        textGrid.append(toAppend)

    if withGrid:
        textDisplay.textGrid = textGrid
        pygame.display.set_caption(saveVal)

        undoMemory = [None,None]
        undoIndex = False
    else:
        titleScreen.textGrid = textGrid

def export():
    global textDisplay, saveVal, cameraSnapProgress

    image = textDisplay.getDisplay()

    if saveVal == None:
        saveVal = 0
        while True:
            if not isfile("projects/project"+str(saveVal)+".bin"): break
            saveVal+=1
        while True:
            if not isfile("projects/project"+str(saveVal)+".png"): break
            saveVal+=1
    if isinstance(saveVal,int):
        saveVal = "project"+str(saveVal)

    pygame.image.save(image, "projects/"+str(saveVal)+".png")

    clicks[5].play()

    cameraSnapProgress = 15

def toggleGrid():
    global gridToggleButton, textDisplay
    for y in range(len(textDisplay.textGrid)):
        for x in range(len(textDisplay.textGrid[y])):
            textDisplay.textGrid[y][x].status = int(gridToggleButton.state)
            textDisplay.textGrid[y][x].char = None

def toggleMusic():
    global musicToggleButton
    pygame.mixer.music.set_volume(int(musicToggleButton.state)*0.3)

def toggleSounds():
    global soundsToggleButton, clicks
    for i in clicks: i.set_volume(int(soundsToggleButton.state)*0.2)

def pickSong():
    global currentSong, alreadyPlayed
    files = listdir("music")
    if len(alreadyPlayed) == len(files): alreadyPlayed = []
    while True:
        song = files[randint(0,len(files)-1)]
        if song[-4:] == ".ogg" and song != "title.ogg" and (not song in alreadyPlayed): break
    currentSong = song
    alreadyPlayed.append(currentSong)
    
    pygame.mixer.music.load("music/"+currentSong)
    pygame.mixer.music.play()

def setUpReset():
    global resetCheck
    resetCheck = True

def cancelReset():
    global resetCheck
    resetCheck = False

def reset():
    global textDisplay, saveVal, resetCheck

    resetCheck = False

    saveVal = None
    
    for y in range(len(textDisplay.textGrid)):
        for x in range(len(textDisplay.textGrid[y])):
            textDisplay.textGrid[y][x].setAll(32,1,0)

    pygame.display.set_caption("unsaved")

def checkInside(n,originalCellInfo):
    global charToggleButton, fgToggleButton, bgToggleButton, textDisplay
    if not ((charToggleButton.getState() and textDisplay.textGrid[n[1]][n[0]].character != originalCellInfo[0]) or (fgToggleButton.getState() and textDisplay.textGrid[n[1]][n[0]].fgcol != originalCellInfo[1]) or (bgToggleButton.getState() and textDisplay.textGrid[n[1]][n[0]].bgcol != originalCellInfo[2])):
        return True
    return False

palette = [(0,0,0),(255,255,255),(31,36,106),(138,17,129),(209,68,68),(44,165,62),(104,203,203),(227,199,45)]
#palette = [(0, 0, 0),(220, 245, 255),(85, 65, 95),(100, 105, 100),(215, 115, 85),(80, 140, 215),(100, 185, 100),(230, 200, 110)]
brightPalette = []
changeBy = (10,20,10)
for i in palette:
    colour = list(i)
    colour[0]+=changeBy[0]
    if colour[0]>255: colour[0] = 255-changeBy[0]
    colour[1]+=changeBy[1]
    if colour[1]>255: colour[1] = 255-changeBy[1]
    colour[2]+=changeBy[2]
    if colour[2]>255: colour[2] = 255-changeBy[2]
    brightPalette.append(tuple(colour))

clicks = [pygame.mixer.Sound("sfx/click2.ogg"),
          pygame.mixer.Sound("sfx/click1.ogg"),
          pygame.mixer.Sound("sfx/splash.ogg"),
          pygame.mixer.Sound("sfx/charselect.ogg"),
          pygame.mixer.Sound("sfx/draw.ogg"),
          pygame.mixer.Sound("sfx/camera.ogg"),
          pygame.mixer.Sound("sfx/fill1.ogg"),
          pygame.mixer.Sound("sfx/fill2.ogg"),
          pygame.mixer.Sound("sfx/undo.ogg"),
          ]
for i in clicks:
    i.set_volume(0.2)

charsTemp = pygame.image.load("kitchen-sink-by-retroshark-and-polyducks.png")
#charsTemp = pygame.image.load("kitchen-bathtub.png")
#charsTemp = pygame.image.load("piggythelad.png")
characterWidth = charsTemp.get_width()//16
characterHeight = charsTemp.get_height()//16
chars = []
toAppend = []
toAppend2 = []
for gridY in range(charsTemp.get_height()//characterHeight):
    for gridX in range(charsTemp.get_width()//characterWidth):
        toAppend2 = []
        for y in range(characterHeight):
            toAppend = []
            for x in range(characterWidth):
                pixel = charsTemp.get_at(((gridX*characterWidth)+x,(gridY*characterHeight)+y))
                if pixel == (0,0,0,255): toAppend.append(False)
                else: toAppend.append(True)
            toAppend2.append(toAppend)
        chars.append(toAppend2)

screen = pygame.display.set_mode((62*characterWidth,36*characterHeight), flags=pygame.SCALED)
pygame.display.set_caption("unsaved")
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("icon.png"))

saveVal = None

textDisplay = TextDisplay(40,32,0)
titleScreen = TextDisplay(40,32,0)
load(False)

brushSelection = TextDisplay(16,16,1)

colourSelection1 = TextDisplay(4,2,2)
colourSelection2 = TextDisplay(4,2,2)

brushDisplayCell = Cell(0)

loadCheck = False
resetCheck = False

screenIndex = 0

undoMemory = [None,None]
currentChanges = []
undoIndex = False

alreadyPressed = []
alreadyClicked = []

fillList = []
stopInput = False

cameraSnapProgress = 0
cameraSnapSurface = pygame.Surface((62*characterWidth,36*characterHeight))
cameraSnapSurface.fill(palette[1])

brushLabel = UIText("Brush: ",1)
FGLabel = UIText("FG: ",1)
BGLabel = UIText("BG: ",1)
brushTypeLabel = UIText("Replace: ",1)
charToggleLabel = UIText("Char ",1)
charToggleButton = UIButton((50,26),0,1,0,True)
fgToggleLabel = UIText("FG ",1)
fgToggleButton = UIButton((50,28),0,1,0,True)
bgToggleLabel = UIText("BG ",1)
bgToggleButton = UIButton((50,30),0,1,0,True)
fillToggleLabel = UIText("Fill ",1)
fillToggleButton = UIButton((50,32),0,1,0,False)
switchColoursButton = UITextButton((49,21),1,"SWITCH",0,1,False,switchColours)
shiftRightButton = UITextButton((59,24),1,chr(26),0,1,False,shiftRight)
shiftUpButton = UITextButton((58,24),1,chr(24),0,1,False,shiftUp)
shiftLeftButton = UITextButton((58,25),1,chr(27),0,1,False,shiftLeft)
shiftDownButton = UITextButton((59,25),1,chr(25),0,1,False,shiftDown)
saveButton = UITextButton((56,27),1,"SAVE",0,1,False,save)
loadButton = UITextButton((56,29),1,"LOAD",0,1,False,setUpLoad)
loadCheckLabel = UIText("Are you sure? Any unsaved changes will be lost.",1)
loadYesButton = UITextButton((51,34),1,"YES",0,1,False,load)
loadNoButton = UITextButton((56,34),1,"NO",0,1,False,cancelLoad)
exportButton = UITextButton((54,31),1,"EXPORT",0,1,False,export)
settingsLabel = UIText("Settings: ",1)
gridToggleButton = UITextButton((2,3),0,"GRID",0,1,True,toggleGrid)
musicToggleButton = UITextButton((2,5),0,"MUSIC "+chr(13),0,1,True,toggleMusic)
soundsToggleButton = UITextButton((2,7),0,"SOUND",0,1,True,toggleSounds)
resetButton = UITextButton((55,1),1,"RESET",0,1,False,setUpReset)
resetYesButton = UITextButton((51,34),1,"YES",0,1,False,reset)
resetNoButton = UITextButton((56,34),1,"NO",0,1,False,cancelReset)
author1Label = UIText("TXTART made by Sam Goff, palette by GooGroker, font by",1)
author2Label = UIText("Polyducks and retroshark.",1)

pygame.mixer.music.set_volume(0.3)

currentSong = "title.ogg"
alreadyPlayed = []
pygame.mixer.music.load(currentSong)
pygame.mixer.music.play(-1)

running = True
while running:
    screen.fill(palette[0])

    if currentSong == "title.ogg" and screenIndex != 0:
        currentSong = "Currently fading..."
        pygame.mixer.music.fadeout(100)
        
    if not pygame.mixer.music.get_busy(): pickSong()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keysPressed = pygame.key.get_pressed()

    if keysPressed[pygame.K_s] and (not stopInput):
        if not "s" in alreadyPressed:
            if screenIndex != 2: screenIndex += 1
            else: screenIndex = 1
            alreadyPressed.append("s")
            clicks[0].play()
    elif "s" in alreadyPressed: alreadyPressed.remove("s")

    if screenIndex == 1:

        textDisplay.draw(characterWidth*2,characterHeight*1)

        brushDisplayImg = brushDisplayCell.getCharImg()
        screen.blit(brushDisplayImg,(51*characterWidth,1*characterHeight))

        brushSelection.draw(44*characterWidth,3*characterHeight)

        colourSelection1.draw(44*characterWidth,21*characterHeight)
        switchColoursButton.draw()
        colourSelection2.draw(56*characterWidth,21*characterHeight)

        brushLabel.draw((44,1))
        FGLabel.draw((44,20))
        BGLabel.draw((56,20))
        brushTypeLabel.draw((44,24))
        charToggleLabel.draw((45,26))
        charToggleButton.draw()
        fgToggleLabel.draw((45,28))
        fgToggleButton.draw()
        bgToggleLabel.draw((45,30))
        bgToggleButton.draw()
        fillToggleLabel.draw((45,32))
        fillToggleButton.draw()
        shiftRightButton.draw()
        shiftUpButton.draw()
        shiftLeftButton.draw()
        shiftDownButton.draw()
        saveButton.draw()
        if loadCheck:
            loadCheckLabel.draw((2,34))
            loadYesButton.draw()
            loadNoButton.draw()
        else: loadButton.draw()
        exportButton.draw()
        if resetCheck:
            loadCheckLabel.draw((2,34))
            resetYesButton.draw()
            resetNoButton.draw()
        else: resetButton.draw()

        if pygame.mouse.get_pressed()[0] and (not stopInput):
            change = False
            
            pos = [0,0]
            mousePos = pygame.mouse.get_pos()
            pos[0] = int(((mousePos[0]-characterWidth*2)/characterWidth))
            pos[1] = int(((mousePos[1]-characterHeight*1)/characterHeight))
            if pos[0]>=0 and pos[0]<40 and pos[1]>=0 and pos[1]<32:
                if (charToggleButton.getState() and textDisplay.textGrid[pos[1]][pos[0]].character != brushDisplayCell.character) or (fgToggleButton.getState() and textDisplay.textGrid[pos[1]][pos[0]].fgcol != brushDisplayCell.fgcol) or (bgToggleButton.getState() and textDisplay.textGrid[pos[1]][pos[0]].bgcol != brushDisplayCell.bgcol):
                    if not "canvas" in alreadyClicked:
                        alreadyClicked.append("canvas")
                        currentChanges = [[],[]]
                    if fillToggleButton.getState():
                        clicks[6].play()
                        originalCellInfo = [textDisplay.textGrid[pos[1]][pos[0]].character,textDisplay.textGrid[pos[1]][pos[0]].fgcol,textDisplay.textGrid[pos[1]][pos[0]].bgcol]
                        fillList = []
                        fillList.append((pos[0],pos[1]))
                        var = 0
                        while fillList != []:
                            n = fillList[0]
                            fillList = fillList[1:]
                            if checkInside(n,originalCellInfo):
                                currentChanges[0].append((n, textDisplay.textGrid[n[1]][n[0]].character, textDisplay.textGrid[n[1]][n[0]].fgcol, textDisplay.textGrid[n[1]][n[0]].bgcol))
                                if charToggleButton.getState(): textDisplay.textGrid[n[1]][n[0]].setChar(brushDisplayCell.character)
                                if fgToggleButton.getState(): textDisplay.textGrid[n[1]][n[0]].setFgcol(brushDisplayCell.fgcol)
                                if bgToggleButton.getState(): textDisplay.textGrid[n[1]][n[0]].setBgcol(brushDisplayCell.bgcol)
                                currentChanges[1].append((n, textDisplay.textGrid[n[1]][n[0]].character, textDisplay.textGrid[n[1]][n[0]].fgcol, textDisplay.textGrid[n[1]][n[0]].bgcol))
                                if n[0]>0:
                                    if randint(0,2) == 2:
                                        if checkInside((n[0]-1,n[1]),originalCellInfo) and n[0]-2>0: fillList.append((n[0]-2,n[1]))
                                    fillList.append((n[0]-1,n[1]))
                                if n[0]<len(textDisplay.textGrid[0])-1:
                                    if randint(0,2) == 2:
                                        if checkInside((n[0]+1,n[1]),originalCellInfo) and n[0]+2<len(textDisplay.textGrid[0])-1: fillList.append((n[0]+2,n[1]))
                                    fillList.append((n[0]+1,n[1]))
                                if n[1]>0:
                                    if randint(0,2) == 2:
                                        if checkInside((n[0],n[1]-1),originalCellInfo) and n[1]-2>0: fillList.append((n[0],n[1]-2))
                                    fillList.append((n[0],n[1]-1))
                                if n[1]<len(textDisplay.textGrid)-1:
                                    if randint(0,2) == 2:
                                        if checkInside((n[0],n[1]+1),originalCellInfo) and n[1]+2<len(textDisplay.textGrid)-1: fillList.append((n[0],n[1]+2))
                                    fillList.append((n[0],n[1]+1))
                                var+=1
                                if var == 20:
                                    textDisplay.draw(characterWidth*2,characterHeight*1)
                                    pygame.display.update()
                                    clock.tick(60)
                                    var = 0
                                
                        clicks[7].play()
                    else:
                        #undoMemory.append(Undo(pos, textDisplay.textGrid[pos[1]][pos[0]].character, textDisplay.textGrid[pos[1]][pos[0]].fgcol, textDisplay.textGrid[pos[1]][pos[0]].bgcol))
                        currentChanges[0].append((pos, textDisplay.textGrid[pos[1]][pos[0]].character, textDisplay.textGrid[pos[1]][pos[0]].fgcol, textDisplay.textGrid[pos[1]][pos[0]].bgcol))
                        #textDisplay.textGrid[pos[1]][pos[0]].setAll(brushDisplayCell.character, brushDisplayCell.fgcol, brushDisplayCell.bgcol)
                        if charToggleButton.getState(): textDisplay.textGrid[pos[1]][pos[0]].setChar(brushDisplayCell.character)
                        if fgToggleButton.getState(): textDisplay.textGrid[pos[1]][pos[0]].setFgcol(brushDisplayCell.fgcol)
                        if bgToggleButton.getState(): textDisplay.textGrid[pos[1]][pos[0]].setBgcol(brushDisplayCell.bgcol)
                        currentChanges[1].append((pos, textDisplay.textGrid[pos[1]][pos[0]].character, textDisplay.textGrid[pos[1]][pos[0]].fgcol, textDisplay.textGrid[pos[1]][pos[0]].bgcol))
                        clicks[4].play()
            
            pos = [0,0]
            pos[0] = int(((mousePos[0]-(44*characterWidth))/characterWidth))
            pos[1] = int(((mousePos[1]-(3*characterHeight))/characterHeight))
            if pos[0]>=0 and pos[0]<16 and pos[1]>=0 and pos[1]<16:
                if not "brushSelect" in alreadyClicked:
                    brushDisplayCell.setChar((pos[1]*16)+pos[0])
                    clicks[3].play()
                    change = True
                    alreadyClicked.append("brushSelect")

            pos = [0,0]
            pos[0] = int(((mousePos[0]-(44*characterWidth))/characterWidth))
            pos[1] = int(((mousePos[1]-(21*characterHeight))/characterHeight))
            if pos[0]>=0 and pos[0]<4 and pos[1]>=0 and pos[1]<2:
                if not "fgSelect" in alreadyClicked:
                    brushDisplayCell.setFgcol((pos[1]*4)+pos[0])
                    clicks[2].play()
                    change = True
                    alreadyClicked.append("fgSelect")

            pos = [0,0]
            pos[0] = int(((mousePos[0]-(56*characterWidth))/characterWidth))
            pos[1] = int(((mousePos[1]-(21*characterHeight))/characterHeight))
            if pos[0]>=0 and pos[0]<4 and pos[1]>=0 and pos[1]<2:
                if not "bgSelect" in alreadyClicked:
                    brushDisplayCell.setBgcol((pos[1]*4)+pos[0])
                    clicks[2].play()
                    change = True
                    alreadyClicked.append("bgSelect")

            if change:
                for y in range(len(brushSelection.textGrid)):
                    for x in range(len(brushSelection.textGrid[y])):
                        brushSelection.textGrid[y][x].setFgcol(brushDisplayCell.fgcol)
                        brushSelection.textGrid[y][x].setBgcol(brushDisplayCell.bgcol)

        else:
            if "brushSelect" in alreadyClicked: alreadyClicked.remove("brushSelect")
            elif "fgSelect" in alreadyClicked: alreadyClicked.remove("fgSelect")
            elif "bgSelect" in alreadyClicked: alreadyClicked.remove("bgSelect")
            elif "canvas" in alreadyClicked:
                alreadyClicked.remove("canvas")
                undoMemory = currentChanges
                undoIndex = False

        if keysPressed[pygame.K_LCTRL] and keysPressed[pygame.K_z] and (not None in undoMemory) and (not "canvas" in alreadyClicked):
            if not "controlz" in alreadyPressed:
                toUndo = undoMemory[int(undoIndex)]
                for i in toUndo:
                    pos = i[0]
                    textDisplay.textGrid[pos[1]][pos[0]].setAll(i[1],i[2],i[3])
                clicks[8].play()
                alreadyPressed.append("controlz")
                undoIndex = not undoIndex
        elif "controlz" in alreadyPressed: alreadyPressed.remove("controlz")

        #coords = [randint(0,31),randint(0,39)]
        #textDisplay.textGrid[coords[0]][coords[1]].setChar(randint(0,255))
        #textDisplay.textGrid[coords[0]][coords[1]].setFgcol(randint(0,7))
        #while True:
        #    textDisplay.textGrid[coords[0]][coords[1]].setBgcol(randint(0,7))
        #    if textDisplay.textGrid[coords[0]][coords[1]].bgcol != textDisplay.textGrid[coords[0]][coords[1]].fgcol: break

    elif screenIndex == 2:

        gridToggleButton.draw()
        settingsLabel.draw((2,1))
        musicToggleButton.draw()
        soundsToggleButton.draw()
        author1Label.draw((2,32))
        author2Label.draw((2,34))

    elif screenIndex == 0:

        titleScreen.draw(characterWidth*10,characterHeight*2)

    if cameraSnapProgress != 0:
        cameraSnapSurface.set_alpha(255*(cameraSnapProgress/20))
        screen.blit(cameraSnapSurface, (0,0))
        cameraSnapProgress-=1

    pygame.display.update()
    #running = False
    clock.tick(60)
pygame.quit()
