

#!/usr/bin/env python
#Written By Daniel Leong, Michael Searing, Saarth Mehrotra, Rahil Dedhia and Adam Coppola

from visual import *
from itertools import permutations
from random import choice
from time import sleep
from Tkinter import *
from SimpleCV import *

fps = 24
speedMult = 4
stage = 0

############
#DATA STUFF#
############
class Side():
    def __init__(self,stickers,name):
        self.stickers = stickers
        self.name = name
    def __str__(self):
        return '%s' % self.stickers
    def getRow(self,row,inv=-1): # object name, row (invertible), indices of elements in row
        stickers = self.stickers[row][::-inv]
        indices = ((row,1+inv),(row,1),(row,1-inv))
        return self.name,stickers,indices
    def getCol(self,col,inv=-1): # object name, column (invertible), indices of elements in column
        stickers = [self.stickers[x][col] for x in (0,1,2)][::-inv]
        indices = ((1+inv,col),(1,col),(1-inv,col))
        return self.name,stickers,indices
    def rotate(self,inv=-1):
        # rotate sides
        assoc = assocFunc(self.name) # associations for side to be rotated
        for trgFace in range(4): # each target face
            num = 0
            srcFace = (trgFace-1 if inv == -1 else trgFace-3) # source face
            for row,col in assoc[trgFace][2]: # each sticker to be affected
                eval(assoc[trgFace][0]).stickers[row][col] = assoc[srcFace][1][num]
                num += 1
        # rotate face
        S = eval(self.name) # current side object
        S.stickers = [S.getCol(1+inv,-inv)[1],
                      [S.stickers[1-inv][1],self.name.lower(),S.stickers[1+inv][1]],
                      S.getCol(1-inv,-inv)[1]]


###########
#GUI STUFF#
###########
def Pplaytime():

    playtime = Toplevel()
    playtime.title("Virtual Rubik's Cube Playground")

    #here is where we include all of the rotate functions.
    rotatelabel = Label(playtime, text="Rotations")
    rotatelabel.grid(row=0, column=0, columnspan= 3)

    whitespace = Label(playtime, text = "     ")
    whitespace.grid(row = 0, column=3)
    whitespace2 = Label(playtime, text = "     ")
    whitespace2.grid(row=0, column=5)

    Rlabel = Label(playtime, text='Or press "r" and "R"')
    Rlabel.grid(row=1,column=2)
    Ylabel = Label(playtime, text='Or press "y" and "Y"')
    Ylabel.grid(row=2,column=2)
    Blabel = Label(playtime, text='Or press "b" and "B"')
    Blabel.grid(row=3,column=2)
    Olabel = Label(playtime, text='Or press "o" and "O"')
    Olabel.grid(row=4,column=2)
    Wlabel = Label(playtime, text='Or press "w" and "W"')
    Wlabel.grid(row=5,column=2)
    Glabel = Label(playtime, text='Or press "g" and "G"')
    Glabel.grid(row=6,column=2)

    rclock=Button(playtime, text='clockwise', bg = 'red', command = lambda : execute('r'))
    rclock.grid(row=1, column=0)
    yclock=Button(playtime, text='clockwise', bg = 'yellow', command = lambda : execute('y'))
    yclock.grid(row=2, column=0)
    bclock=Button(playtime, text='clockwise', bg = 'blue', command = lambda : execute('b'))
    bclock.grid(row=3, column=0)
    oclock=Button(playtime, text='clockwise', bg = 'orange', command = lambda : execute('o'))
    oclock.grid(row=4, column=0)
    wclock=Button(playtime, text='clockwise', bg = 'white', command = lambda : execute('w'))
    wclock.grid(row=5, column=0)
    gclock=Button(playtime, text='clockwise', bg = 'green', command = lambda : execute('g'))
    gclock.grid(row=6, column=0)
    Rcounterclock=Button(playtime, text='counterclockwise', bg = 'red', command = lambda : execute('R'))
    Rcounterclock.grid(row=1, column=1)
    Ycounterclock=Button(playtime, text='counterclockwise', bg = 'yellow', command = lambda : execute('Y'))
    Ycounterclock.grid(row=2, column=1)
    Bcounterclock=Button(playtime, text='counterclockwise', bg = 'blue', command = lambda : execute('B'))
    Bcounterclock.grid(row=3, column=1)
    Ocounterclock=Button(playtime, text='counterclockwise', bg = 'orange', command = lambda : execute('O'))
    Ocounterclock.grid(row=4, column=1)
    Wcounterclock=Button(playtime, text='counterclockwise', bg = 'white', command = lambda : execute('W'))
    Wcounterclock.grid(row=5, column=1)
    Gcounterclock=Button(playtime, text='counterclockwise', bg = 'green', command = lambda : execute('G'))
    Gcounterclock.grid(row=6, column=1)

    #here is where we include all of the change view functions.
    viewlabel = Label(playtime, text="View Corners")
    viewlabel.grid(row=0, column = 4)

    aview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('ryb'))
    aview.grid(row=2,column=4)

    bview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('ryg'))
    bview.grid(row=3,column=4)

    cview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('rwg'))
    cview.grid(row=4,column=4)

    dview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('owg'))
    dview.grid(row=5,column=4)

    eview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('owb'))
    eview.grid(row=6,column=4)

    fview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('oyb'))
    fview.grid(row=7,column=4)

    gview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('oyg'))
    gview.grid(row=8,column=4)

    hview = Button(playtime, text="switch camera angle", command = lambda : camera_angle('rwb'))
    hview.grid(row=1,column=4)

    #here is where we include buttons that direct to help
    helplabel = Label(playtime, text="HELP")
    helplabel.grid (row = 0, column=6)

    randomizer = Button(playtime, text = "Randomize the cube!", command = scramble)
    randomizer.grid(row=2, column=6)

    whatnext = Button(playtime, text = "What's the next step?", command = lambda : printer('This would pop up a window with the series of tutorials'))
    whatnext.grid(row=1, column=6)

    #mainscreen = Button(playtime, text= "Return to main screen", command = lambda : Gohome(playtime))
    #mainscreen.grid(row=5,column=6)

    solver = Button(playtime, text = "Fully Solve!", command = Solve)
    solver.grid(row=3,column=6)

    while stage == 1 or stage == 3:
        playtime.mainloop()

def Popener():

    opener = Tk()
    opener.title("Virtual Rubik's Cube")

    introduction = Label(opener, text="Welcome to your virtual Rubik's Cube. To get started, please choose and option below")
    introduction.grid(row=0, rowspan=2, column=0, columnspan=3)

    startbutton = Button(opener, text="Play with a cube", command= lambda : changestagetoone(opener))
    startbutton.grid(row=2,column=1)

    importbutton = Button(opener, text="Import a real life cube to play with", command= lambda : changestagetotwo(opener))
    importbutton.grid(row=3, column=1)

    # tutorialbutton = Button(opener, text="Teach me how to solve a cube", command = lambda : printer("This would bring them to the collection of tutorial pages"))
    # tutorialbutton.grid(row=4, column=1)

   # racebutton = Button(opener, text="Race against a computer!", command = lambda : printer("this would bring up a computer solving cube and a randomized cube, hopefully by expo"))
   # racebutton.grid(row=5, column=1)

    while stage == 0:
        opener.mainloop()

def Pcvinstructions():

    cvinstructions = Tk()
    cvinstructions.title("How to import your cube")

    cvtext = Label(cvinstructions, text = "Here is where you can import a cube to play with.\n To do so, you will be taking pictures of each side of your cube.\n Hold your cube up to your webcam so that the center square in the camera matches your cube's center square.\n The center of the side facing up should match colors with the up arrow on the screen.\n Make sure all nine dots become the same color as your nine squares.\n Click to take the picture, and repeat for each side.")
    cvtext.pack()

    cvinstructions.mainloop()

def printer(text):
    print(text)

def changestagetoone(window):
    global stage
    stage = 1
    window.destroy()

def changestagetotwo(window):
    global stage
    stage = 2
    window.destroy()

#################
#MORE DATA STUFF#
#################
def printCube():
    for side in [R,Y,B,O,W,G]: print(side)

def printAssoc():
    for side in 'RYBOWG': print(side,assocFunc(side))

# what a rotation on each side affects, in clockwise order
# args: layer to check, selection inversion
def assocFunc(name, lay = 0):
    if name == 'R': return Y.getCol(lay),G.getCol(lay),W.getRow(lay,1),B.getRow(lay,1)
    if name == 'Y': return B.getCol(lay),O.getCol(lay),G.getRow(lay,1),R.getRow(lay,1)
    if name == 'B': return R.getCol(lay),W.getCol(lay),O.getRow(lay,1),Y.getRow(lay,1)
    if name == 'O': return B.getRow(2-lay),W.getRow(2-lay),G.getCol(2-lay,1),Y.getCol(2-lay,1)
    if name == 'W': return R.getRow(2-lay),G.getRow(2-lay),O.getCol(2-lay,1),B.getCol(2-lay,1)
    if name == 'G': return Y.getRow(2-lay),O.getRow(2-lay),W.getCol(2-lay,1),R.getCol(2-lay,1)

##########
### AI ###
##########
def isCross(name, layer = False): # check side (or layer) for cross
    associations = assocFunc(name)
    stickers = eval(name).stickers
    isCross = False
    if stickers[0][1] == stickers[1][0] == stickers[1][1] == stickers[1][2] == stickers[2][1]:
        isCross = True
        if layer:
            for side in associations:
               if side[0].lower() != side[1][1]: isCross = False
    return isCross

def isComplete(name): # check side for complete
    stickers = eval(name).stickers
    isCorrect = True
    for row in stickers:
        for sticker in row:
            if sticker != stickers[1][1]:
                isCorrect = False
    return isCorrect

def isLayer(name, lay=0): # check layer for complete
    isLayer = True
    associations = assocFunc(name, lay)
    if lay == 0: # if checking first layer, also check side
        if not isComplete(name): isLayer = False
    for side in associations:
        lowerSide = side[0].lower()
        if lowerSide != side[1][0] or lowerSide != side[1][2]: isLayer = False
    return isLayer

def isCornersAligned(name): # check if 4 corners are in right place on face
    return len([getCornerList[x][0] for x in range(8) if name in getCornerList[x][0]]) == 4

def isDone(): # check cube for complete
    isDone = True
    for name in 'RYBOWG':
        if not isComplete(name): isDone = False
    return isDone

# Function (in progress) to check how far along the cube is.
def howFarAlong():
    bestSide = ['w', 'nothing', 0]
    for name in 'RYBOWG':
        otherName = 'RYBOWG'['RYBOWG'.index(name)-3]

        progress,points = 'none', 0
        if isCross(name, True): # check bottom layer for cross
            progress,points = 'cross', 1
        if isLayer(name) and points > 0: # check first layer for complete
            progress,points = 'first layer', 2
        if isLayer(name, 1) and points > 1: # check second layer for complete
            progress,points = 'second layer', 3
        if isCross(otherName) and points > 2: # check top side for cross
            progress,points = 'top cross', 4
        if isCross(otherName, True) and points > 3: # check top layer for cross
            progress,points = 'top cross aligned', 5
        if isDone() and points > 4: # check entire cube for complete
            progress,points = 'Complete!', 6

        if points > bestSide[2]: # find most solved side
            bestSide = [name, progress, points]
    return bestSide


def getCornerList(): # list of corner cubies, top and bottom clockwise from top
    return [['YRB',Y.stickers[0][0]+R.stickers[0][0]+B.stickers[0][0]],
            ['YBO',Y.stickers[0][2]+B.stickers[2][0]+O.stickers[0][0]],
            ['YOG',Y.stickers[2][2]+O.stickers[2][0]+G.stickers[0][2]],
            ['YGR',Y.stickers[2][0]+G.stickers[0][0]+R.stickers[0][2]],
            ['WRB',W.stickers[0][0]+R.stickers[2][0]+B.stickers[0][2]],
            ['WBO',W.stickers[2][0]+B.stickers[2][2]+O.stickers[0][2]],
            ['WOG',W.stickers[2][2]+O.stickers[2][2]+G.stickers[2][2]],
            ['WGR',W.stickers[0][2]+G.stickers[2][0]+R.stickers[2][2]]]

def isCornersAligned(name): # check if 4 corners are in right place on face
    return len([getCornerList[x][0] for x in range(8) if name in getCornerList[x][0]]) == 4

def isCorners(): # check corners for position and orientation
    corners,res = getCornerList(),[[],[]]
    for x in range(8):
        if set(corners[x][1]) == set(corners[x][0].lower()):
            res[0] += [x]
        if corners[x][1] == corners[x][0].lower():
            res[1] += [x]
    return res

def getCornerDict(inv=1):
    return dict([getCornerList()[x][::inv] for x in range(8)])

cubieName = 'YBYOYGYRRBBOOGGRWBWOWGWR' # side name for each side cubie
cubieRow = '011120101020211111211202' # row for each side cubie
cubieCol = '102011010111120202122111' # col for each side cubie
def getSideDict(): # list of side cubies
    sideCubieDict = dict()
    for x in range(12):
        s1 = eval(cubieName[2*x]).stickers[int(cubieRow[2*x])][int(cubieCol[2*x])]
        s2 = eval(cubieName[2*x+1]).stickers[int(cubieRow[2*x+1])][int(cubieCol[2*x+1])]
        sideCubieDict[cubieName[2*x:2*x+2]] = s1+s2 # all possible input/output combinations
        sideCubieDict[cubieName[2*x:2*x+2][::-1]] = s2+s1
        sideCubieDict[s1+s2] = cubieName[2*x:2*x+2]
        sideCubieDict[s2+s1] = cubieName[2*x:2*x+2][::-1]
    return sideCubieDict

def reorder(iStr,permuted,original): # reorder input string according to permutation
    pattern = [permuted.index(original[x]) for x in range(len(iStr))] # original->permuted index map
    return ''.join([iStr[pattern[x]] for x in range(len(iStr))])

def findCubie(c): # input position or stickers, return stickers or position
    sideDict = getSideDict() # input side
    if len(c) == 2:
        return sideDict[c]
    cornerDict = getCornerDict() # input corner position
    if len(c) == 3 and c.upper() == c:
        for permutation in permutations(c):
            permuted = ''.join(permutation)
            try: return reorder(cornerDict[permuted],permuted,c)
            except: continue
    cornerDict = getCornerDict(-1) # input corner stickers
    if len(c) == 3 and c.lower() == c:
        for permutation in permutations(c):
            permuted = ''.join(permutation)
            try: return reorder(cornerDict[permuted],permuted,c)
            except: continue
    print('Not valid side or corner')


###############
### SOLVER  ###
###############
def scramble():
    for x in range(30):
        execute(choice('rybowgRYBOWG'))

def crossCompleter(search):
    # A function that will complete the cross of a given face
    assocSearch = assocFunc(search)
    otherName = 'RYBOWG'['RYBOWG'.index(search)-3]
    assocSides = [assocSearch[0][0],assocSearch[1][0],assocSearch[2][0],assocSearch[3][0]]
    # creating the side cubie identies. 
    sideIdentities = []
    for i in range(4): sideIdentities.append(search.lower()+assocSides[i].lower())
    for Identity in sideIdentities:
        sideLocation = findCubie(Identity)
        if search not in sideLocation and otherName not in sideLocation:
            # The following code finds the associated sides of the target side.
            assocTargetSides = []
            sidesAroundTarget = assocFunc(sideLocation[1])
            for i in range(4): assocTargetSides.append(sidesAroundTarget[i][0])
            if (assocTargetSides.index(search)-assocTargetSides.index(sideLocation[0]))%4 == 1: putUpRotation = sideLocation[1].lower()
            else: putUpRotation = sideLocation[1]
            # This means that the cube is on the middle band
            numberAwayCW = (assocSides.index(sideLocation[1])-assocSides.index(Identity[1].capitalize()))%4
            numberAwayCCW = 4-numberAwayCW
            if numberAwayCCW > numberAwayCW:
                move = numberAwayCW * search.lower()+putUpRotation+numberAwayCW*search
            else:
                move = numberAwayCCW * search + putUpRotation + numberAwayCCW*search.lower()
        elif search in sideLocation:
            if search == sideLocation[0]:
                # the piece on on the top i.e. it's correct.
                numberAwayCW = (assocSides.index(sideLocation[1])-assocSides.index(Identity[1].capitalize()))%4
                numberAwayCCW = 4- numberAwayCW
                if numberAwayCW == 0:
                    move = ''
                elif numberAwayCCW > numberAwayCW:
                    move = sideLocation[1].lower() + numberAwayCW * search.lower() + sideLocation[1] + numberAwayCW * search
                else:
                    move = sideLocation[1].lower() + numberAwayCCW * search + sideLocation[1] + numberAwayCCW * search.lower()
                #Then, we'd rotate the side sideLocation[1], orient the top layer, and then rotate sideLocation[1] the other direction
            else:
                numberAwayCW = (assocSides.index(Identity[1].capitalize())-assocSides.index(sideLocation[0])-1)%4
                numberAwayCCW = 4 - numberAwayCW
                if numberAwayCCW > numberAwayCW:
                    move = numberAwayCW * search.lower() + assocSides[assocSides.index(Identity[1].capitalize())-1]+numberAwayCW*search+Identity[1].capitalize()
                else:
                    move = numberAwayCCW * search + assocSides[assocSides.index(Identity[1].capitalize())-1]+numberAwayCCW*search.lower()+Identity[1].capitalize()
                # I'll explain this case later
                ##########DONE TO THIS STEP
        else:
            if otherName == sideLocation[0]:
                numberAwayCW = (assocSides.index(sideLocation[1])-assocSides.index(Identity[1].capitalize()))%4
                numberAwayCCW = 4-numberAwayCW
                if numberAwayCCW > numberAwayCW:
                    move = numberAwayCW * otherName.lower()+Identity[1]*2
                else:
                    move = numberAwayCCW * otherName + Identity[1]*2                
                # Align the side, then rotate the side up twice
            else:
                numberAwayCW = (assocSides.index(sideLocation[0])-assocSides.index(Identity[1].capitalize())+1)%4
                sideNextDoor = assocSides[assocSides.index(Identity[1].capitalize())-1]
                # defines the side clockwise of the side that I need.
                numberAwayCCW = 4-numberAwayCW
                if numberAwayCCW > numberAwayCW:
                    move = numberAwayCW * otherName.lower()+sideNextDoor.lower()+Identity[1].capitalize()+sideNextDoor
                else:
                    move = numberAwayCCW * otherName + sideNextDoor.lower()+Identity[1].capitalize()+sideNextDoor
                # Align the side to right next to the place we need, then bring it up.
        # print(Identity, move)
        execute(move)

def cornerSolver(search):
    assocSearch = assocFunc(search)
    otherName = 'RYBOWG'['RYBOWG'.index(search)-3]
    assocSides = [assocSearch[0][0],assocSearch[1][0],assocSearch[2][0],assocSearch[3][0]]
    # creating the side cubie identies. 
    for i in range(4): 
        # iterating through each corner, solving them individually
        currentCorner = search.lower()+assocSides[i-1].lower()+assocSides[i].lower()
        cornerLocation = findCubie(currentCorner)
        if cornerLocation.lower() == currentCorner:
            move = ''
        else:
            movePartOne = orientCorner(currentCorner, cornerLocation, search, otherName, assocSides)
            execute(movePartOne)
            newLocation = findCubie(currentCorner)
            movePartTwo = placeCorner(currentCorner, newLocation, search, otherName, assocSides)
            execute(movePartTwo)
                # the the search piece is on the bottom. 
            # This if tree will solve all of the corner situations in which the corner is located on the bottom layer. 

def orientCorner(currentCorner, cornerLocation, search, otherName, assocSides):
    if search in cornerLocation:
        # This if tree will solve all of the corner situations in which the corner is located on the top layer
        if cornerLocation[0].lower() == currentCorner[0]:
            return cornerLocation[1]+otherName+cornerLocation[1].lower()
        elif cornerLocation[1].lower() == currentCorner[0]:
            return cornerLocation[0].lower()+otherName.lower()+cornerLocation[0]
        else:
            return cornerLocation[0]+otherName+cornerLocation[0].lower()
        # if the corner is on the top layer
    else: 
        if cornerLocation[0] == otherName:
            Id = assocSides.index(currentCorner[2].capitalize())
            Lo = assocSides.index(cornerLocation[2])
            numberAwayCW = (Lo - Id + 1)%4
            numberAwayCCW = 4 - numberAwayCW
            if numberAwayCW < numberAwayCCW:
                return numberAwayCW*otherName.lower() + currentCorner[1].upper() + otherName.lower() + currentCorner[1].lower()
            else:
                return numberAwayCCW*otherName + currentCorner[1].upper() + otherName.lower() + currentCorner[1].lower()
        else:
            return ''

def placeCorner(currentCorner, cornerLocation, search, otherName, assocSides):
    if cornerLocation[1] == otherName:
        # left insert case
        Id = assocSides.index(currentCorner[2].capitalize())
        Lo = assocSides.index(cornerLocation[2])
        sideNextDoor = assocSides[assocSides.index(currentCorner[2].upper())-1]
        numberAwayCW = (Lo - Id)%4
        numberAwayCCW = 4 - numberAwayCW
        if numberAwayCW < numberAwayCCW:
            return numberAwayCW*otherName.lower() + sideNextDoor + otherName + sideNextDoor.lower()
        else:
            return numberAwayCCW*otherName + sideNextDoor + otherName + sideNextDoor.lower()
    else:
        # right insert case
        Id = assocSides.index(currentCorner[1].capitalize())
        Lo = assocSides.index(cornerLocation[1])
        sideNextDoor = assocSides[(assocSides.index(currentCorner[1].upper())+1)%4]
        numberAwayCW = (Lo - Id)%4
        numberAwayCCW = 4 - numberAwayCW
        if numberAwayCW < numberAwayCCW:
            return numberAwayCW*otherName.lower() + sideNextDoor.lower() + otherName.lower() + sideNextDoor
        else:
            return numberAwayCCW*otherName + sideNextDoor.lower() + otherName.lower() + sideNextDoor

def layerTwoSolver(search):
    # input the top layer and it will solve the corresponding layer 2 for you.
    assocSearch = assocFunc(search)
    otherName = 'RYBOWG'['RYBOWG'.index(search)-3]
    assocSides = [assocSearch[0][0],assocSearch[1][0],assocSearch[2][0],assocSearch[3][0]]
    layerTwoSides = []
    for i in range(4): layerTwoSides.append(assocSides[i-1].lower()+assocSides[i].lower())
    # creating the layer2 side objects
    for side in layerTwoSides:
        sideLocation = findCubie(side)
        if side.upper() == sideLocation:
            movePartOne = 'Done'
        else:
            if search in sideLocation:
                movePartOne = ''
            else:
                movePartOne  = toTopLayer(sideLocation, search, layerTwoSides)
            execute(movePartOne)
            newLocation = findCubie(side)
            movePartTwo = toMiddleLayer(side, newLocation, search, assocSides, layerTwoSides)
            execute(movePartTwo)

def toTopLayer(sideLocation, search, layerTwoSides):
    # will take a side cubie located on the middle layer and bring it up to the top layer
    leftInsert = 'ULulufUF'
    if sideLocation.lower() in layerTwoSides:
        # checking orientation of the side cubie
        return algorithmInterpreter(sideLocation[0], search, leftInsert)
    else:
        return algorithmInterpreter(sideLocation[1], search, leftInsert)

def toMiddleLayer(side, newLocation, search, assocSides, layerTwoSides):
    # This takes side cubes on the top layer and puts them where they should be in the middle layer. 
    indexForOrientation = newLocation.index(search)-1
    targetSide = side[indexForOrientation].upper()
    currentSide = newLocation[indexForOrientation]
    leftInsert = 'ULulufUF'
    rightInsert = 'urURUFuf'
    if (assocSides.index(side[indexForOrientation-1].upper()) - assocSides.index(targetSide))%4 == 1: 
        moveIn = leftInsert
    else:
        moveIn = rightInsert 
    numberAwayCCW = (assocSides.index(newLocation[indexForOrientation])-assocSides.index(targetSide))%4
    numberAwayCW = 4-numberAwayCCW
    if numberAwayCCW > numberAwayCW:
        move = numberAwayCW * search.lower() + algorithmInterpreter(targetSide, search, moveIn)
    else:
        move = numberAwayCCW * search + algorithmInterpreter(targetSide, search, moveIn)
    return move

def execute(moves):
        for key in moves:
            updateData(key) # run data rotation
            updateVisual(key) # run visual rotation

def algorithmInterpreter(front,top,algorithm):
    assocSearch = assocFunc(front)
    assocSides = [assocSearch[0][0],assocSearch[1][0],assocSearch[2][0],assocSearch[3][0]]
    clockwiseRotations = 'frubld'
    cubeOrientation = {}
    cubeOrientation['F'] = front
    cubeOrientation['U'] = top
    cubeOrientation['B'] = 'RYBOWG'['RYBOWG'.index(front)-3]
    cubeOrientation['D'] = 'RYBOWG'['RYBOWG'.index(top)-3]
    cubeOrientation['L'] = assocSides[assocSides.index(top)-1]
    cubeOrientation['R'] = assocSides[assocSides.index(top)-3]
    parsedAlgorithm = ''
    for turn in algorithm:
        move = cubeOrientation[turn.upper()]
        if turn in clockwiseRotations: move = move.lower()
        parsedAlgorithm += move
    return parsedAlgorithm

def fruRUF(R,U,F):
    execute([F.lower(),R.lower(),U.lower(),R,U,F])
def ruRuruuR(R,U):
    execute([R.lower(),U.lower(),R,U.lower(),R.lower(),U.lower(),U.lower(),R])
def urULuRUl(R,U,L):
    execute([U.lower(),R.lower(),U,L,U.lower(),R,U,L.lower()])
def RDrdRDrd(R,D):
    execute(2*[R,D,R.lower(),D.lower()])

def topCross(top):
    stickerList = [eval(top).stickers[x[0]][x[1]] for x in ((0,1),(1,2),(2,1),(1,0))] # cross
    if stickerList.count(top.lower()) == 4: # already cross
        pass
    elif top.lower() not in stickerList: # nothing
        fruRUF(assocFunc(top)[2][0],top,assocFunc(top)[3][0]) # get L
        fruRUF(assocFunc(top)[0][0],top,assocFunc(top)[1][0]) # get line
        fruRUF(assocFunc(top)[0][0],top,assocFunc(top)[1][0]) # get cross
    elif top.lower() == stickerList[stickerList.index(top.lower())-2]: # already line
        lIndex = stickerList.index(top.lower()) # index of line (left)
        fruRUF(assocFunc(top)[lIndex-2][0],top,assocFunc(top)[lIndex-1][0]) # get cross
    else: # already L
        lIndex = ''.join(stickerList+[stickerList[0]]).index(2*top.lower()) # index of L (left)
        fruRUF(assocFunc(top)[lIndex-2][0],top,assocFunc(top)[lIndex-1][0]) # get line
        fruRUF(assocFunc(top)[lIndex-2][0],top,assocFunc(top)[lIndex-1][0]) # get cross
    stickerList = ''.join([assocFunc(top)[x][1][1] for x in range(4)]) # side stickers
    sideList = ''.join([assocFunc(top)[x][0] for x in range(4)])
    if sideList.lower() == stickerList: # already oriented
        pass
    elif stickerList in (2*sideList).lower(): # already oriented, needs rotation
        cIndex = (2*sideList).index(stickerList.upper()) # index of cross
        if cIndex <= 2: execute(top.lower()*cIndex) # CW to get oriented
        else: execute(top) # CCW to get oriented
    elif stickerList[0] == 'rybowg'['rybowg'.index(stickerList[2])-3]: # already line
        if stickerList[0] == sideList[0].lower() or stickerList[1] == sideList[1].lower(): # already aligned
            ruRuruuR(assocFunc(top)[(3 if stickerList[0] == sideList[0].lower() else 2)][0],top)
            ruRuruuR(assocFunc(top)[(0 if stickerList[0] == sideList[0].lower() else 3)][0],top)
        else:
            execute(top) # get oriented
            ruRuruuR(assocFunc(top)[(3 if stickerList[1] == sideList[0].lower() else 2)][0],top)
            ruRuruuR(assocFunc(top)[(0 if stickerList[1] == sideList[0].lower() else 3)][0],top)
        execute(top.lower()) # CW to finish
    else: # already L
        for x in range(4):
            if stickerList[x:x+2] in 2*sideList.lower(): break # find ordered side pair (L)
        lIndex = (2*sideList).index(stickerList[x:x+2].upper()) # index of L
        delta = (x-lIndex+4)%4 # actual - desired
        if delta <= 2: execute(top+top) # CCW to get oriented
        else: execute(top.lower()) # CW to get oriented
        ruRuruuR(assocFunc(top)[lIndex-3][0],top) # get oriented
        execute(top.lower()) # CW to finish

def getCorners(top,orientation=False):
    corners = [top+assocFunc(top)[x][0]+(2*assocFunc(top))[x+1][0] for x in range(4)]
    correct = []
    for corner in corners:
        if orientation and corner.lower() == findCubie(corner): correct += [corner]
        elif not orientation and set(corner.lower()) == set(findCubie(corner)): correct += [corner]
    return corners,correct

def topCorners(top):
    corners,correct = getCorners(top)
    if len(correct) != 4: # not all already positioned
        if len(correct) == 0: # none positioned
            urULuRUl(assocFunc(top)[0][0],top,assocFunc(top)[2][0])
            corners,correct = getCorners(top)
        if len(correct) == 1: # one positioned
            cIndex = corners.index(correct[0]) # index of correct corner
            urULuRUl(assocFunc(top)[cIndex][0],top,assocFunc(top)[cIndex-2][0])
            if len(getCorners(top)[1]) == 1: # still only one positioned
                urULuRUl(assocFunc(top)[cIndex][0],top,assocFunc(top)[cIndex-2][0])
        corners,correct = getCorners(top,True)
    for cIndex in range(4):
        if corners[cIndex] not in correct: break
    corner = corners[cIndex] # location where all solving will occur
    while len(getCorners(top,True)[1]) != 4: # not entirely solved
        while corner.index(top) != findCubie(corner).index(top.lower()): # current cubie isn't solved
            RDrdRDrd(assocFunc(top)[cIndex][0],'RYBOWG'['RYBOWG'.index(top)-3])
        while corner.index(top) == findCubie(corner).index(top.lower()) and len(getCorners(top,True)[1]) != 4:
            execute(top.lower())

def moveTrimmer(movestring):
    moveList = []
    for move in movestring: moveList.append(move)
    for i in range(0, len(moveList)-1):
        if moveList[i] == moveList[i+1] == moveList[i+2]:
            if moveList[i] == moveList[i].upper():
                moveList[i], moveList[i+1], moveList[i+2]= moveList[i].lower(), '', ''
            else:
                moveList[i], moveList[i+1], moveList[i+2]= moveList[i].upper(), '', ''
    for i in range(0,len(moveList)-1):
        if moveList[i] == moveList[i+1].lower() or moveList[i].lower() == moveList[i+1]:
            moveList[i], moveList[i+1] = '', ''
    return ''.join(moveList)

#############
### OTHER ###
#############
def updateData(key):
    if key == key.lower(): eval(key.upper()).rotate() # lowercase -> clockwise
    if key == key.upper(): eval(key).rotate(1) # uppercase -> counterclockwise

def updateVisual(key):
    face_color,axis = faces[key.lower()]
    angle = ((pi/2) if key.isupper() else -pi/2)
    for r in arange(0, angle, angle/fps):
        rate(speedMult*fps)
        for sticker in stickers:
            if dot(sticker.pos, axis) > 0.5:
                sticker.rotate(angle=angle/fps,axis=axis,origin=(0,0,0))

def Solve():
    sideToSolve = howFarAlong()[0].upper()
    topSide = 'RYBOWG'['RYBOWG'.index(sideToSolve)-3]
    lbl = label(yoffset=200, text="Solving"+sideToSolve+"Side", line=0)
    crossCompleter(sideToSolve)
    cornerSolver(sideToSolve)
    layerTwoSolver(topSide)
    topCross(topSide)
    topCorners(topSide)

def tutorial():
    sideToSolve = howFarAlong()
    helpDict = {'first layer': ("U'L'ULUFU'F'", "URU'R'U'F'UF"), 'second layer': ("FRUR'U'F"), 'top cross': ("RUR'URUUR'"), 'top cross aligned':("URU'L'UR'U'L")}
    print('The side that is furthest along is the ' + sideToSolve[0].upper() + ' side. Currently, the '+sideToSolve[1]+ ' is complete.') 
    if sideToSolve[1] in helpDict:    
        print('Useful algorithms for this stage of the cube are '+helpDict[sideToSolve[1]]+'.')
    print("Press 'h' for an algorithm guide. Press key" + str(sideToSolve[0]+1)+ " to finish this step. Press t at any time to refresh the tutorial")
    key = scene.kb.getkey()
    if key.lower() == 'h': Print('Algorithms are the main method of solving a Rubiks Cube. The letter refers to what face the user is supposed to rotate and the apostrophe refers to direction of rotation')
    if key.lower() == 't': tutorial()

def camera_angle(side):
    if set(side) == set(['r','y','g']):
        scene.forward = (-1.1,-.8,1)
    if set(side) == set(['g','w','o']):
        scene.forward = (1.1,.8,1)
    if set(side) == set(['r','w','g']):
        scene.forward = (-1.1,.8,1)
    if set(side) == set(['o','y','b']):
        scene.forward = (1.1,-.8,-1)
    if set(side) == set(['b','y','r']):
        scene.forward = (-1.1,-.8,-1)
    if set(side) == set(['b','w','r']):
        scene.forward = (-1.1,.8,-1)
    if set(side) == set(['g','y','o']):
        scene.forward = (1.1,-.8,1)
    if set(side) == set(['o','w','b']):
        scene.forward = (-1.1,.8,-1) 

#################
#IMPORTING STUFF#
#################

def compare(colors):
    #Function returns the color of a sticker based on its rgb value
    #colors are in order RYBOWG
    red = 150, 52.0, 77.66666666666667
    blue = 10.666666666666666, 50, 125
    green = 7.666666666666667, 118.66666666666667, 79.33333333333333
    white = 140, 155.11111111111111, 176.55555555555554
    yellow = 140, 150.66666666666666, 61.22222222222222
    orange = 160, 112.44444444444444, 48.0
    coloravgs = (red,yellow,blue,orange,white,green)
    r,g,b = colors
    error=1000
    for i in range(6):
        ravg,gavg,bavg = coloravgs[i]
        error2 = abs(r-ravg)+abs(g-gavg)+abs(b-bavg)
        if error2 < error:
            error=error2
            index=i
    RYBOWG = 'rybowg'
    point = RYBOWG[index] #assign point to a color using index of the min error
    return point

def compare2(pack,img):
    #Function returns the color of a sticker based on its rgb value 2.0
    r,g,b = img[pack]
    #colors are in order RYBOWG
    red = 150, 52.0, 77.66666666666667
    blue = 10.666666666666666, 50, 125
    green = 7.666666666666667, 118.66666666666667, 79.33333333333333
    white = 140, 155.11111111111111, 176.55555555555554
    yellow = 140, 150.66666666666666, 61.22222222222222
    orange = 160, 112.44444444444444, 48.0
    coloravgs = (red,yellow,blue,orange,white,green)
    error=1000
    for i in range(6):
        ravg,gavg,bavg = coloravgs[i]
        error2 = abs(r-ravg)+abs(g-gavg)+abs(b-bavg)
        if error2 < error:
            error=error2
            index=i
    RYBOWG = 'rybowg'
    point = RYBOWG[index] #assign point to a color using index of the min error
    return point

def side(colors):
    #Function runs the compare function for all 9 stickers of a side and
    #returns them in one list
    c1,c2,c3,c4,c5,c6,c7,c8,c9=colors
    t1=compare(c1)
    t2=compare(c2)
    t3=compare(c3)
    m1=compare(c4)
    m2=compare(c5)
    m3=compare(c6)
    b1=compare(c7)
    b2=compare(c8)
    b3=compare(c9)
    face=[[t1,t2,t3],[m1,m2,m3],[b1,b2,b3]]
    return face

def middlecolor(m2,img,length):
    #Function takes in the side and prints that color on the center sticker 
    points = [(length*3,length*2),(length*4,length*2),(length*4,length*3),(length*3,length*3)]
    if m2 == "r" or m2 == "red" or m2 == "R" or m2 == "Red" or m2 == "RED":
        img.dl().polygon(points, filled=True, color = Color.RED)
        return("red")
    if m2 == "b" or m2 == "blue" or m2 == "B" or m2 == "Blue" or m2 == "BLUE":
        img.dl().polygon(points, filled=True, color = Color.BLUE)
        return("blue")
    if m2 == "g" or m2 == "green" or m2 == "G" or m2 == "Green" or m2 == "GREEN":
        img.dl().polygon(points, filled=True, color = Color.GREEN)
        return("green")
    if m2 == "y" or m2 == "yellow" or m2 == "Y" or m2 == "Yellow" or m2 == "YELLOW":
        img.dl().polygon(points, filled=True, color = Color.YELLOW)
        return("yellow")
    if m2 == "o" or m2 == "orange" or m2 == "O" or m2 == "Orange" or m2 == "ORANGE":
        img.dl().polygon(points, filled=True, color = Color.ORANGE)
        return("orange")
    if m2 == "w" or m2 == "white" or m2 == "W" or m2 == "White" or m2 == "WHITE":
        img.dl().polygon(points, filled=True, color = Color.WHITE)
        return("white")

def top_arrow(top_color,img,length):
    #Function takes in the top color and prints that color in an arrow 
    points = [(length*3,length*.75),(length*3,length*.5),(length*2.5,length*.5),(length*3.5,length*.1),(length*4.5,length*.5),(length*4,length*.5),(length*4,length*.75)]
    if top_color == "r" or top_color == "red" or top_color == "R" or top_color == "Red" or top_color == "RED":
        img.dl().polygon(points, filled=True, color = Color.RED)
    if top_color == "b" or top_color == "blue" or top_color == "B" or top_color == "Blue" or top_color == "BLUE":
        img.dl().polygon(points, filled=True, color = Color.BLUE)
    if top_color == "g" or top_color == "green" or top_color == "G" or top_color == "Green" or top_color == "GREEN":
        img.dl().polygon(points, filled=True, color = Color.GREEN)
    if top_color == "y" or top_color == "yellow" or top_color == "Y" or top_color == "Yellow" or top_color == "YELLOW":
        img.dl().polygon(points, filled=True, color = Color.YELLOW)
    if top_color == "o" or top_color == "orange" or top_color == "O" or top_color == "Orange" or top_color == "ORANGE":
        img.dl().polygon(points, filled=True, color = Color.ORANGE)
    if top_color == "w" or top_color == "white" or top_color == "W" or top_color == "White" or top_color == "WHITE":
        img.dl().polygon(points, filled=True, color = Color.WHITE)  

def checkpixel(pixel,img):
    #Function allows live color interpretation by running a compare function
    y=compare2(pixel,img)
    for i in range(1,10):
        if y == 'r':
            img.dl().circle((pixel), i, Color.RED)
        if y == 'b':
            img.dl().circle((pixel), i, Color.BLUE)        
        if y == 'g':
            img.dl().circle((pixel), i, Color.GREEN)
        if y == 'y':
            img.dl().circle((pixel), i, Color.YELLOW)    
        if y == 'o':
            img.dl().circle((pixel), i, Color.ORANGE)
        if y == 'w':
            img.dl().circle((pixel), i, Color.WHITE)

def check_center_pixel(pixels,img):
    #Function allows live color interpretation by running a compare function
    y=compare2(pixels[4],img)
    if y == 'r': return("red")
    if y == 'b': return("blue")      
    if y == 'g': return("green")
    if y == 'y': return("yellow")
    if y == 'o': return("orange")
    if y == 'w': return("white")
    
def startcamera(m2,top_color):
    #Function starts the camera and returns the output of the side function
    cam = Camera() #starts the camera
    disp = Display() #starts the display
    while disp.isNotDone(): #displays continuous stream
        img = cam.getImage().flipHorizontal()
        length=img.width/7 #divides the screen into 7 components
        #Creates a reference square
        points = [(length*2,length*1),(length*2,length*4),(length*5,length*4),(length*5,length*1)]
        img.dl().polygon(points, color=Color.BLACK)
        #Calls the function to print the color in the middle square
        midcolor = middlecolor(m2,img,length)
        #Calls the function to print the color of the top square ARROW
        top_arrow(top_color,img,length)
        #Identifies where the stickers should line up using circles
        pixels = [(length*2.5,length*1.5),(length*2.5,length*2.5),(length*2.5,length*3.5),(length*3.5,length*1.5),(length*3.5,length*2.5),(length*3.5,length*3.5),(length*4.5,length*1.5),(length*4.5,length*2.5),(length*4.5,length*3.5)]
        #Live display of color of pixel
        for pixel in pixels:
            checkpixel(pixel,img)
        img.show()
        midpixel = check_center_pixel(pixels,img)
        if disp.mouseLeft and midcolor == midpixel: #If left cursor is clicked, break out of the loop
            break
    #Assigns rgb values to each sticker after break
    t1 = rt1,gt1,bt1 = img[pixels[0]]
    t2 = rt2,gt2,bt2 = img[pixels[3]]
    t3 = rt3,gt3,bt3 = img[pixels[6]]
    m1 = rm1,gm1,bm1 = img[pixels[1]]
    m2 = rm2,gm2,bm2 = img[pixels[4]]
    m3 = rm3,gm3,bm3 = img[pixels[7]]
    b1 = rb1,gb1,bb1 = img[pixels[2]]
    b2 = rb2,gb2,bb2 = img[pixels[5]]
    b3 = rb3,gb3,bb3 = img[pixels[8]]
    face_colors = (t1,t2,t3,m1,m2,m3,b1,b2,b3)
    face = side(face_colors)
    return face

def average(m2):
    t1,t2,t3,m1,m2,m3,b1,b2,b3 = startcamera(m2)
    rt1,gt1,bt1 = t1
    rt2,gt2,bt2 = t2
    rt3,gt3,bt3 = t3
    rm1,gm1,bm1 = m1
    rm2,gm2,bm2 = m2
    rm3,gm3,bm3 = m3
    rb1,gb1,bb1 = b1
    rb2,gb2,bb2 = b2
    rb3,gb3,bb3 = b3
    r=(rt1+rt2+rt3+rm1+rm2+rm3+rb1+rb2+rb3)/9
    g=(gt1+gt2+gt3+gm1+gm2+gm3+gb1+gb2+gb3)/9
    b=(bt1+bt2+bt3+bm1+bm2+bm3+bb1+bb2+bb3)/9
    return r,g,b

def getcolors():
    R = startcamera("r","y")
    Y = startcamera("y","b")
    B = startcamera("b","r")
    O = startcamera("o","b")
    W = startcamera("w","r")
    G = startcamera("g","y")
    cube = [R,Y,B,O,W,G]
    print('cube')
    print(type(cube))
    print(cube)
    return cube

def namestocolors(cube):
    for eachside in cube:
        sidecolors = []
        for eachrow in eachside:
            for eachsquare in eachrow:
                if eachsquare == 'r': sidecolors.append(color.red)
                if eachsquare == 'y': sidecolors.append(color.yellow)
                if eachsquare == 'b': sidecolors.append(color.blue)
                if eachsquare == 'o': sidecolors.append(color.orange)
                if eachsquare == 'w': sidecolors.append(color.white)
                if eachsquare == 'g': sidecolors.append(color.green)
        if eachside[1][1] == 'r': redcolors = sidecolors
        if eachside[1][1] == 'y': yellowcolors = sidecolors
        if eachside[1][1] == 'b': bluecolors = [sidecolors[0],sidecolors[3],sidecolors[6],
                                                sidecolors[1],sidecolors[4],sidecolors[7],
                                                sidecolors[2],sidecolors[5],sidecolors[8]]
        if eachside[1][1] == 'o': orangecolors = [sidecolors[0],sidecolors[3],sidecolors[6],
                                                sidecolors[1],sidecolors[4],sidecolors[7],
                                                sidecolors[2],sidecolors[5],sidecolors[8]]
        if eachside[1][1] == 'w': whitecolors = [sidecolors[0],sidecolors[3],sidecolors[6],
                                                sidecolors[1],sidecolors[4],sidecolors[7],
                                                sidecolors[2],sidecolors[5],sidecolors[8]]
        if eachside[1][1] == 'g': greencolors = sidecolors


    faces = {'r': (redcolors, (1, 0, -1), (1, 0, -1), (1, 0, 0)),
            'y': (yellowcolors, (-1, 0, 1), (-1, 0, 1), (0, 1, 0)),
            'b': (bluecolors, (-1, 0, 1), (1, 0, -1), (0, 0, 1)),
            'o': (orangecolors, (-1, 0, 1), (1, 0, -1), (-1, 0, 0)),
            'w': (whitecolors, (-1, 0, 1), (1, 0, -1), (0, -1, 0)),
            'g': (greencolors, (-1, 0, 1), (-1, 0, 1), (0, 0, -1))}

    return faces

############
### MAIN ###
############

while stage == 0:

    Popener()

print("out of stage 0")

#if we want to start with basic
if stage == 1:

    #########################
    ### DATA MANIPULATION ###
    #########################

#if we want to import
if stage == 2:

    Pcvinstructions()

    cube = getcolors()

    faces = namestocolors(cube)


    # Create colored stickers on each face, one cubie at a time.
    stickers = []
    print('good so far')
    for face_colors, ys, xs, axis in faces.itervalues():
        print("facecolors")
        print(face_colors)
        squarecount = 0
        for y in ys:
            for x in xs:
                sticker = box(color=face_colors[squarecount], pos=(x, y, 1.5), length=0.98, height=0.98, width=0.05)
                cos_angle = dot((0, 0, 1), axis)
                pivot = (cross((0, 0, 1), axis) if cos_angle == 0 else (1, 0, 0))
                sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=(0, 0, 0))
                stickers.append(sticker)
                squarecount += 1

while True:
    key = scene.kb.getkey() # keyboard input
    if key.lower() == '0': scramble()
    if key.lower() == '1': crossCompleter('W')
    if key.lower() == '2': cornerSolver('W')
    if key.lower() == '3': layerTwoSolver('Y')
    if key.lower() == '4': topCross('Y')
    if key.lower() == '5': topCorners('Y')
    if key.lower() == '6': tutorial
    if key.lower() == '9': Solve()
    if faces.has_key(key.lower()): # input matches any side
        execute(key) # make move
    Pplaytime()
