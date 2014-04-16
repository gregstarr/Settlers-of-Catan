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

BOARDWIDTH = 640
BOARDHEIGHT = 480

# Main game function
def main():

    pygame.init()

    global gamewindow, coords, buildings, buttons, tiles
    
    gamewindow = pygame.display.set_mode((BOARDWIDTH,BOARDHEIGHT))

    # Buttons for city and road
    buildcitybutton=buildButton('city',100,450,60,20)
    buildroadbutton=buildButton('road',30,450,60,20)

    # keeps track of mouse position    
    mousex = 0
    mousey = 0

    coords=makeCoord() #list of coordinates, (x,y,status)
    buildings=[] # list of all the buildings, (type,point or points)
    tiles=makeTiles() # list of resource tiles
    buttons=[buildcitybutton,buildroadbutton] # list of buttons

    buildings.append(construction('road',[19,26]))

    # fix building cities so that you can't build cities next to each other
    # make resources


    # happens constantly
    while True:

        
        drawBoard() #function that keeps the board updated

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

        # selecting points
        point=getCoord(mousex,mousey,coords)
        if point!=None and mouseClicked==True:
            if coords[point].selected==False:
                coords[point].selected=True
            else:
                coords[point].selected=False

        # building cities
        if buildcitybutton.checkForMouse(mousex,mousey)==True and mouseClicked==True:
            buildcitybutton.buildcity()

        # building roads
        if buildroadbutton.checkForMouse(mousex,mousey)==True and mouseClicked==True:
            buildroadbutton.buildroad()


        pygame.display.set_caption(str(point)+' '+str(mousex)+' '+str(mousey))                
        pygame.display.update()

def makeCoord(): # sets up initial coordinates
    coords=[]
    keeps='00011000011001101001100101100110100110010110011000011000'
    
    for x in range(BOARDWIDTH)[60::90]:
        for y in range(BOARDHEIGHT)[20::60]:
            coords.append(coordinate(x,y,0))
    for cord in coords:
        if keeps[coords.index(cord)]=='1':
            cord.status=1
        
    return coords

def getCoord(x,y,coords):
    # returns which coordinate the mouse is
    # over (when passed the mouse's coordinates)
    
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
        pygame.draw.polygon(gamewindow,resourceTile.colors[resourceTile.resources.index(tile.rec)],plist)
        pygame.draw.polygon(gamewindow,white,plist,5)


    for butt in buttons:
        pygame.draw.rect(gamewindow,butt.boxcolor,butt.box)
        txtobj=pygame.font.Font(None,30)
        txt=txtobj.render(butt.function,False,butt.fontcolor)
        gamewindow.blit(txt,butt.box)
        
    for cord in coords:
        cord.update()
        if cord.status!=0:
            pygame.draw.circle(gamewindow,cord.color,(cord.x,cord.y),4)
        
    for structure in buildings:
        if structure.kind=='city':
            x=coords[structure.points[0]].x
            y=coords[structure.points[0]].y
            pygame.draw.lines(gamewindow,purple,True,[(x+6,y+6),(x-1,y-8),(x-7,y+6)],3)

        if structure.kind=='road':
            x1=coords[structure.points[0]].x
            y1=coords[structure.points[0]].y
            x2=coords[structure.points[1]].x
            y2=coords[structure.points[1]].y
            pygame.draw.line(gamewindow,black,(x1,y1),(x2,y2),7)

class buildButton:
    # class for buttons, keeps track of
    # function(road or city) and where the button is
    
    def __init__(self,function,left,top,width,height):
        self.function = function
        self.box=pygame.Rect((left,top),(width,height))
        self.boxcolor=blue
        self.fontcolor=yellow

    def checkForMouse(self,x,y): # returns whether mouse is touching button
        if self.box.collidepoint(x,y):
            return True
        return False

    def buildcity(self): # builds a city
        citynear=False
        selected=[]
        
        for cord in coords: # check for selected coordinates
            if cord.selected==True:
                selected.append(cord)
        
        for city in buildings: # check for cities within 1 space
            if city.kind=='city':
                if abs(city.points[0]-coords.index(selected[0])) in [1,7,9]:
                    citynear=True

        if citynear==False and selected[0].status==2: # if the space is buildable, then build
            buildings.append(construction('city',[coords.index(selected[0])]))
            selected[0].selected=False
        else:
            selected[0].selected=False


    def buildroad(self): # builds a road
        points=[]
        if self.function=='road':
            for cord in coords:
                if cord.selected==True:
                    points.append(coords.index(cord))
                    
        a=points[0]
        b=0
        if len(points)>1:
            b=points[1]
        
        if (coords[a].status==2 or coords[b].status==2) and (abs(a-b) in [1,7,9]) and len(points)>1:
            buildings.append(construction('road',[a,b]))
            coords[a].selected=False
            coords[b].selected=False
        else:
            coords[a].selected=False
            coords[b].selected=False

        
class construction: # class to keep track of buildings (road,city)
    def __init__(self,kind,points):
        self.kind=kind
        self.points=points

class resourceTile: # class to keep track of resource tiles (hexagons)
    resources=['wheat','wood','brick','stone']
    colors=[(227,169,34),(176,121,58),(212,91,51),(168,168,168)]
    diceNumbers=[3,4,5,6,7,8,9]
    N=0
    
    def __init__(self,points):
        self.points=points
        self.num=resourceTile.N
        resourceTile.N+=1
        self.rec=random.choice(resourceTile.resources)
        self.dice=resourceTile.diceNumbers[self.num]
        self.box=((coords[points[0]].x+70,coords[points[0]].y),(40,40))

def makeTiles():
    tiles=[]
    for a in [3,9,13,19,25,29,35]:
        tiles.append(resourceTile([a,a+7,a+16,a+17,a+10,a+1]))
    return tiles
   

class coordinate: # class for the coordinates

    colors=[white,black,green,red]

    def __init__(self,x,y,status=0):
        self.x=x
        self.y=y
        self.status=status
        self.color=coordinate.colors[self.status]
        self.selected=False

    def update(self):
        # changes color if selected, changes
        # status if connected by road
        roads=0
        for road in buildings:
            if road.kind=='road':
                if coords.index(self) in road.points:
                    roads+=1
        if roads==1:
            self.status=2
        if self.selected==True:
            self.color=blue
        else:
            self.color=coordinate.colors[self.status]


if __name__ == '__main__':
    main()
