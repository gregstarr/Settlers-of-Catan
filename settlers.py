import pygame, sys
from pygame.locals import *

# Colors
black = (0,0,0)
white = (255,255,255)
grey = (120,120,120)
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

    global gamewindow, coords, buildings, buttons
    
    gamewindow = pygame.display.set_mode((BOARDWIDTH,BOARDHEIGHT))

    # Buttons for city and road
    buildcitybutton=buildButton('city',100,450,60,20)
    buildroadbutton=buildButton('road',30,450,60,20)

    # keeps track of mouse position    
    mousex = 0
    mousey = 0

    coords=makeCoord() #list of coordinates, (x,y,status)
    buildings=[] # list of all the buildings, (type,point or points)
    buttons=[buildcitybutton,buildroadbutton]

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


        pygame.display.set_caption(str(point))                
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
    
    for butt in buttons:
        pygame.draw.rect(gamewindow,butt.boxcolor,butt.box)
        txtobj=pygame.font.Font(None,30)
        txt=txtobj.render(butt.function,False,butt.fontcolor)
        gamewindow.blit(txt,butt.box)
        
    for cord in coords:
        cord.update()
        pygame.draw.circle(gamewindow,cord.color,(cord.x,cord.y),5)
        
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
            pygame.draw.line(gamewindow,grey,(x1,y1),(x2,y2),3)

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
        if self.function=='city':
            for cord in coords:
                if cord.status==2 and cord.selected==True:
                    buildings.append(construction('city',[coords.index(cord)]))
                    cord.selected=False
                else:
                    cord.selected=False

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
