# Make the trading system, also make sure you can trade in
# 4 resources of one kind for 1 of another

import pygame, sys, random
from pygame.locals import *

# Colors
black = (0,0,0)
white = (255,255,255)
grey = (99,99,99)
blue = (0,0,255)
red = (255,0,0)
green = (20,230,20)
purple = (255,0,255)
yellow = (255,255,0)

BOARDWIDTH = 800
BOARDHEIGHT = 600

# Main game function
def main():

    pygame.init()

    global gamewindow, error, coords, buildings, buttons, tiles, turncount, players, currentplayer, dice
    
    gamewindow = pygame.display.set_mode((BOARDWIDTH,BOARDHEIGHT))

    # Buttons for city and road
    buildcitybutton=buildButton('city',100,480,60,20)
    buildroadbutton=buildButton('road',30,480,60,20)
    nextTurnButton=buildButton('next turn',30,510,130,40)
    nextTurnButton.boxcolor=green

    # keeps track of mouse position    
    mousex = 0
    mousey = 0

    coords=makeCoord() #list of coordinates, (x,y,status)
    buildings=[] # list of all the buildings, (type,point or points)
    tiles=makeTiles() # list of resource tiles
    buttons=[buildcitybutton,buildroadbutton,nextTurnButton] # list of buttons
    

    setupButtons=[]
    for i in range(5)[2:]:
        setupButtons.append(buildButton(i,130+i*45,400,40,40))

    screen = 'instructions'
    players = []
    currentplayer = 0
    dice=0
    turncount=0
    errorTimer=0
    error=False


    # happens constantly
    while True:

        mouseClicked = False

        # quitting and mouse position updater
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseClicked = True

        if screen == 'instructions':

            gamewindow.fill(white)
            
            welcomeBox=(40,20,560,50)
            welcomeText=pygame.font.Font(None,55)
            welcome=welcomeText.render('Welcome to Settlers of Catan',False,purple)
            gamewindow.blit(welcome,welcomeBox)

            textBox=(40,80,560,560)
            textObj=pygame.font.Font(None,30)
            text=textObj.render("Build roads by selecting 2 points and clicking 'road'",False,black)
            gamewindow.blit(text,textBox)

            textBox=(40,120,560,560)
            textObj=pygame.font.Font(None,30)
            text=textObj.render("Build cities by selecting a point and clicking 'city'",False,black)
            gamewindow.blit(text,textBox)

            textBox=(40,160,560,560)
            textObj=pygame.font.Font(None,30)
            text=textObj.render("You will start with 2 roads and 2 cities",False,black)
            gamewindow.blit(text,textBox)

            textBox=(40,200,560,560)
            textObj=pygame.font.Font(None,30)
            text=textObj.render("They are placed randomly, good luck",False,black)
            gamewindow.blit(text,textBox)            

            textBox=(40,240,560,560)
            textObj=pygame.font.Font(None,30)
            text=textObj.render("Each city will give you one point, first player to ten points wins",False,black)
            gamewindow.blit(text,textBox)

            instBox=(150,350,440,50)
            instText=pygame.font.Font(None,30)
            instruction=instText.render('Choose how many players:',False,grey)
            gamewindow.blit(instruction,instBox)

            for button in setupButtons:
                pygame.draw.rect(gamewindow,yellow,button.box)
                txtobj=pygame.font.Font(None,30)
                txt=txtobj.render(str(button.function),False,black)
                gamewindow.blit(txt,button.box)
                if button.checkForMouse(mousex,mousey)==True and mouseClicked==True:
                    for i in range(button.function):
                        players.append(player(i))
                        currentplayer=button.function-1
                    screen = 'main'
                    startWithRandomBuildings()

            instBox=(650,550,440,50)
            instText=pygame.font.Font(None,23)
            instruction=instText.render('Greg, Steven, Zhao',False,grey)
            gamewindow.blit(instruction,instBox)


        if screen == 'main':
            
            drawBoard() #function that keeps the board updated
        
            # selecting points
            point=getCoord(mousex,mousey)
            if point!=None and mouseClicked==True:
                if coords[point].selected==False:
                    coords[point].selected=True
                else:
                    coords[point].selected=False

            # building cities
            if buildcitybutton.checkForMouse(mousex,mousey)==True and mouseClicked==True:
                buildcity()

            # building roads
            if buildroadbutton.checkForMouse(mousex,mousey)==True and mouseClicked==True:
                buildroad()

            if nextTurnButton.checkForMouse(mousex,mousey)==True and mouseClicked==True:
                nextTurn()

            if error==True:
                errorTimer+=1

                textBox=(600,60,560,20)
                textObj=pygame.font.Font(None,30)
                text=textObj.render("You can't do that!",False,black)
                gamewindow.blit(text,textBox)

            if errorTimer>60:
                error=False
                errorTimer=0

                


            pygame.display.set_caption(str(point)+' '+str(mousex)+' '+str(mousey))                
        pygame.display.update()

def makeCoord(): # sets up initial coordinates
    coords=[]
    keeps='000001100000000110011000011001100110100110011001011001100110100110011001011001100110100110011001011001100110000110011000000001100000'
    
    for x in range(640)[60::53]:
        for y in range(480)[20::39]:
            coords.append(coordinate(x,y))
    for cord in coords:
        if keeps[coords.index(cord)]=='1':
            cord.status.add(5)
        
    return coords

def startWithRandomBuildings():
    
    choosePoints=[]
    initial=[50,74,39,63,87,40,64,88,29,53,77,30,54,78,102,43,67,91,44,68,92,57,81]
    serpentine=[]
    used=[0]
    for i in range(len(players)):
        serpentine.append(i)
        serpentine.append(i)
        
    for cord in coords:
        if 5 in cord.status:
            choosePoints.append(coords.index(cord))
            
    for player in serpentine:

        use=True

        point=random.choice(initial)

        for a in used:
            if (point-a) in [1,11,13,-1,-11,-13]:
                use=False
                
        while use==False:
            test=[]
            point=random.choice(initial)
            for a in used:
                test.append(point-a)
            use=True
            for a in test:
                if a in [1,11,13,-1,-11,-13]:
                    use=False
            
            textBox=(300,500,400,50)
            textObj=pygame.font.Font(None,30)
            gamewindow.fill(white)
            text=textObj.render("Loading... randomizing player {}".format(player+1),False,blue)
            gamewindow.blit(text,textBox)
            pygame.display.update()
            
        used.append(point)
        initial.remove(point)
        
        point2=0
        while point2 not in choosePoints:
            
            point2=point+random.choice([1,11,13,-1,-11,-13])

            textBox=(300,500,400,50)
            textObj=pygame.font.Font(None,30)
            gamewindow.fill(white)
            text=textObj.render("Loading... randomizing player {}".format(player+1),False,blue)
            gamewindow.blit(text,textBox)
            pygame.display.update()

        
        road=construction('road',[point,point2])
        road.player=player
        city=construction('city',[point])
        city.player=player
        buildings.append(city)
        buildings.append(road)
                               

def getCoord(x,y):
    
    for cord in coords:
        left = cord.x -3
        top = cord.y - 3
        coordbox = pygame.Rect((left,top),(6,6))
        if coordbox.collidepoint(x,y):
            return coords.index(cord)
    return None

def drawBoard(): # draws and updates the board
    gamewindow.fill(white)

    for tile in tiles:
        plist=[]
        for p in tile.points:
            plist.append((coords[p].x,coords[p].y))
        if tile.dice==0:
            pygame.draw.polygon(gamewindow,(168,30,8),plist)
        else:
            pygame.draw.polygon(gamewindow,resourceTile.colors[resourceTile.resources.index(tile.rec)],plist)
        pygame.draw.polygon(gamewindow,white,plist,5)
        diceNumObj=pygame.font.Font(None,30)
        diceNum=diceNumObj.render(str(tile.dice),False,black)
        gamewindow.blit(diceNum,tile.box)


    for butt in buttons:
        pygame.draw.rect(gamewindow,butt.boxcolor,butt.box)
        txtobj=pygame.font.Font(None,30)
        txt=txtobj.render(butt.function,False,butt.fontcolor)
        gamewindow.blit(txt,butt.box)
        
        
    for structure in buildings:
        if structure.kind=='city':
            x=coords[structure.points[0]].x
            y=coords[structure.points[0]].y
            pygame.draw.lines(gamewindow,players[structure.player].color,True,[(x+6,y+6),(x-1,y-8),(x-7,y+6)],3)

        if structure.kind=='road':
            x1=coords[structure.points[0]].x
            y1=coords[structure.points[0]].y
            x2=coords[structure.points[1]].x
            y2=coords[structure.points[1]].y
            pygame.draw.line(gamewindow,players[structure.player].color,(x1,y1),(x2,y2),7)

    # display of resources, players, points
    playerTxtBox=(240,480,80,20)
    playerTxtObj=pygame.font.Font(None,30)
    playerTxt=playerTxtObj.render('player|',False,black)
    gamewindow.blit(playerTxt,playerTxtBox)

    resourceTxtBox=(310,480,80,20)
    resourceTxtObj=pygame.font.Font(None,30)
    resourceTxt=resourceTxtObj.render('resources |',False,black)
    gamewindow.blit(resourceTxt,resourceTxtBox)

    pointsTxtBox=(420,480,80,20)
    pointsTxtObj=pygame.font.Font(None,30)
    pointsTxt=pointsTxtObj.render('points',False,black)
    gamewindow.blit(pointsTxt,pointsTxtBox)

    
    
    for i in range(len(players)):

        if i==currentplayer:
            pygame.draw.line(gamewindow,green,(245,517+20*i),(255,517+20*i),5)
        numBox=(260,510+20*i,15,15)
        numTxt=pygame.font.Font(None,30)
        num=numTxt.render(str(i+1),False,players[i].color)
        gamewindow.blit(num,numBox)
        
        wheatBox=(315,510+20*i,15,15)
        pygame.draw.rect(gamewindow,resourceTile.colors[0],wheatBox)
        wheatTxt=pygame.font.Font(None,15)
        wheatNum=wheatTxt.render(str(players[i].rec['wheat']),False,black)
        gamewindow.blit(wheatNum,wheatBox)
        
        brickBox=(335,510+20*i,15,15)
        pygame.draw.rect(gamewindow,resourceTile.colors[2],brickBox)
        brickTxt=pygame.font.Font(None,15)
        brickNum=brickTxt.render(str(players[i].rec['brick']),False,black)
        gamewindow.blit(brickNum,brickBox)
        
        stoneBox=(355,510+20*i,15,15)
        pygame.draw.rect(gamewindow,resourceTile.colors[3],stoneBox)
        stoneTxt=pygame.font.Font(None,15)
        stoneNum=stoneTxt.render(str(players[i].rec['stone']),False,black)
        gamewindow.blit(stoneNum,stoneBox)
        
        woodBox=(375,510+20*i,15,15)
        pygame.draw.rect(gamewindow,resourceTile.colors[1],woodBox)
        woodTxt=pygame.font.Font(None,15)
        woodNum=woodTxt.render(str(players[i].rec['wood']),False,black)
        gamewindow.blit(woodNum,woodBox)
        
        pointsBox=(440,510+20*i,15,15)
        pointsTxt=pygame.font.Font(None,15)
        pointsNum=pointsTxt.render(str(players[i].points),False,black)
        gamewindow.blit(pointsNum,pointsBox)

    # dice roll box
    diceTxtBox=(30,455,60,20)
    diceTxt=pygame.font.Font(None,30)
    diceNum=diceTxt.render('Dice Number: {}'.format(dice),False,black)
    gamewindow.blit(diceNum,diceTxtBox)

    turnTxtBox=(10,10,60,20)
    turnTxt=pygame.font.Font(None,30)
    turnNum=turnTxt.render('Turn: {}'.format(turncount),False,black)
    gamewindow.blit(turnNum,turnTxtBox)

    for cord in coords:
        cord.update()
        if len(cord.status)>0:
            pygame.draw.circle(gamewindow,cord.color,(cord.x,cord.y),4)

def nextTurn():

        global currentplayer, dice, turncount

        
        currentplayer+=1
        if currentplayer>len(players)-1:
            currentplayer=0
            turncount+=1

        # roll dice
        diceroll = random.randint(1,6)+random.randint(1,6)
        dice=diceroll
        
        # allocate resources
        for tile in tiles:
            if tile.dice==diceroll:
                for building in buildings:
                    if building.kind=='city':
                        if building.points[0] in tile.points:
                            players[building.player].rec[tile.rec]+=1

                            
class buildButton:
    # class for buttons, keeps track of
    # function(road or city) and where the button is
    
    def __init__(self,function,left,top,width,height):
        self.function = function
        self.box=pygame.Rect((left,top),(width,height))
        self.boxcolor=grey
        self.fontcolor=black

    def checkForMouse(self,x,y): # returns whether mouse is touching button
        if self.box.collidepoint(x,y):
            return True
        return False
        

def buildcity(): # builds a city
    global error
    citynear=False
    selected=[]
        
    for cord in coords: # check for selected coordinates
        if cord.selected==True:
            selected.append(cord)
        
    for city in buildings: # check for cities within 1 space
        if city.kind=='city':
            if abs(city.points[0]-coords.index(selected[0])) in [0,1,11,13]:
                citynear=True

    if citynear==False and currentplayer+1 in selected[0].status: # if the space is buildable, then build
        if players[currentplayer].rec['wheat']>=1 and players[currentplayer].rec['stone']>=1 and players[currentplayer].rec['wood']>=1 and players[currentplayer].rec['brick']>=1:
            buildings.append(construction('city',[coords.index(selected[0])]))
            players[currentplayer].rec['wheat']-=1
            players[currentplayer].rec['stone']-=1
            players[currentplayer].rec['brick']-=1
            players[currentplayer].rec['wood']-=1
            players[currentplayer].points+=1
        else:
            error=True
    else:
        error=True
    selected[0].selected=False


def buildroad(): # builds a road
    global error
    points=[]
    for cord in coords:
        if cord.selected==True:
            points.append(coords.index(cord))
                
    a=points[0]
    b=0
    if len(points)>1:
        b=points[1]

    roads=[]
    for road in buildings:
        if road.kind=='road':
            roads.append(set(road.points))
    
    if (currentplayer+1 in coords[a].status or currentplayer+1 in coords[b].status) and set([a,b]) not in roads and (abs(a-b) in [1,11,13]) and len(points)>1 and players[currentplayer].rec['brick']>=1 and players[currentplayer].rec['wood']>=1:
        buildings.append(construction('road',[a,b]))
        players[currentplayer].rec['wood']-=1
        players[currentplayer].rec['brick']-=1
    else:
        error=True
    coords[a].selected=False
    coords[b].selected=False
    

        
class construction: # class to keep track of buildings (road,city)

    global currentplayer
    
    def __init__(self,kind,points):
        self.kind=kind
        self.points=points
        self.player=currentplayer

class resourceTile: # class to keep track of resource tiles (hexagons)
    resources=['wheat','wood','brick','stone']
    recdic={'wheat':0,'wood':0,'brick':0,'stone':0}
    colors=[(227,169,34),(176,121,58),(212,91,51),(168,168,168)]
    diceNumbers=[6,4,6,3,5,3,5,11,2,0,8,9,4,10,9,10,8,11,12]
    N=0
    
    def __init__(self,points):
        self.points=points
        self.num=resourceTile.N
        resourceTile.N+=1
        choose=[]
        for rec in resourceTile.recdic:
            if resourceTile.recdic[rec]<4:
                choose.append(rec)
        if len(choose)>0:
            self.rec=random.choice(choose)
        else:
            self.rec=random.choice(resourceTile.resources)
        resourceTile.recdic[self.rec]+=1
        
        self.dice=resourceTile.diceNumbers[self.num]
        self.box=((coords[points[0]].x+45,coords[points[0]].y+10),(40,40))

def makeTiles():
    tiles=[]
    for a in [5,15,25,19,29,39,49,33,43,53,63,73,57,67,77,87,81,91,101]:
        tiles.append(resourceTile([a,a+11,a+24,a+25,a+14,a+1]))
    return tiles

class player:

    colors = [red,purple,green,yellow]

    def __init__(self,num):
         self.num = num
         self.points = 2
         self.rec={'wheat':0,'wood':0,'brick':0,'stone':0}
         self.color=player.colors[num]
   

class coordinate: # class for the coordinates

    colors=[white,red,purple,green,yellow,black]

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.status=set()
        self.color=black
        self.selected=False

    def update(self):
        # changes color if selected, changes
        # status if connected by road
        for road in buildings:
            if road.kind=='road':
                if coords.index(self) in road.points:
                    self.status.add(road.player+1)
        if self.selected==True:
            self.color=blue
        else:
            self.color=black


if __name__ == '__main__':
    main()
