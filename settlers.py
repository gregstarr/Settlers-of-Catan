import pygame, sys
from pygame.locals import *

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (20,230,20)
purple = (255,0,255)
yellow = (255,255,0)

BOARDWIDTH = 640
BOARDHEIGHT = 480

def main():

    pygame.init()

    global gamewindow
    
    gamewindow = pygame.display.set_mode((BOARDWIDTH,BOARDHEIGHT))
    buildcitybutton=buildButton('city',100,440,60,20)
    
    mousex = 0
    mousey = 0

    coords=makeCoord() #list of coordinates, (x,y,status)
    buildings=[] # list of all the buildings, (type,point or points)

    # figure out the road code, make it so a single road starts in the middle
    # then build from there, get the roads and cities to work according to the
    # rules, then work on developing resources


    
    while True:

        
        drawBoard(coords,buildings)

        mouseClicked = False

        # events, quitting
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
            if buildcitybutton.pressed==True:
                buildcitybutton.pressed=False
            else:
                buildcitybutton.pressed=True
                buildcitybutton.buildcity(coords,buildings)


        pygame.display.set_caption(str(point))
        buildcitybutton.update()

                
        pygame.display.update()

def makeCoord():
    coords=[]
    keeps='00011000011001101001100101100110100110010110011000011000'
    
    for x in range(BOARDWIDTH)[60::90]:
        for y in range(BOARDHEIGHT)[20::60]:
            coords.append(coordinate(x,y,0))
    for cord in coords:
        if keeps[coords.index(cord)]=='1':
            cord.status=2
        
    return coords

def getCoord(x,y,coords):
    for cord in coords:
        left = cord.x -3
        top = cord.y - 3
        coordbox = pygame.Rect((left,top),(6,6))
        if coordbox.collidepoint(x,y):
            return coords.index(cord)
    return None


def drawBoard(coords,construction):
    gamewindow.fill(white)
    for cord in coords:
        cord.update()
        pygame.draw.circle(gamewindow,cord.color,(cord.x,cord.y),5)
    for building in construction:
        if building.kind=='city':
            pygame.draw.circle(gamewindow,purple,(coords[building.points[0]].x,coords[building.points[0]].y),3)

class buildButton:
    
    def __init__(self,function,left,top,width,height):
        self.function = function
        self.pressed = False
        self.box=pygame.Rect((left,top),(width,height))
        self.boxcolor=green
        self.fontcolor=yellow

    def checkForMouse(self,x,y):
        if self.box.collidepoint(x,y):
            return True
        return False

    def buildcity(self,coords,buildings):
        if self.function=='city':
            for cord in coords:
                if cord.status==2 and cord.selected==True:
                    cord.status=3
                    buildings.append(construction('city',[coords.index(cord)]))
                    self.pressed=False
                    cord.selected=False
                else:
                    cord.selected=False
                    self.pressed=False

    def buildroad(self,coords,a,b):
        if self.function=='road':
            coords[a].status,coords[b].status=4
            self.pressed=False

    def update(self):
        if self.pressed==True:
            self.boxcolor=yellow
            self.fontcolor=green
        else:
            self.boxcolor=green
            self.fontcolor=yellow
            
        pygame.draw.rect(gamewindow,self.boxcolor,self.box)
        txtobj=pygame.font.Font(None,30)
        txt=txtobj.render(self.function,False,self.fontcolor)
        gamewindow.blit(txt,self.box)
        
class construction:
    def __init__(self,kind,points):
        self.kind=kind
        self.points=points
        

class coordinate:

    colors=[white,black,green,red]

    def __init__(self,x,y,status=0):
        self.x=x
        self.y=y
        self.status=status
        self.color=coordinate.colors[self.status]
        self.selected=False

    def update(self):
        if self.selected==True:
            self.color=blue
        else:
            self.color=coordinate.colors[self.status]


if __name__ == '__main__':
    main()
