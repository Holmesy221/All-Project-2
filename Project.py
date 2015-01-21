from tkinter import *
import collections, random, time, sys
from math import sqrt
from Queues import *
from Worlds import *
from Treasures import *
from Landmarks import *

#================= Search Algorithm ======================

def FindRobotPath(World,startpoint,goal):
    frontier = Queue()
    frontier.put(startpoint)
    came_from = {}
    came_from[startpoint] = None

    while not frontier.empty():
        current = frontier.get()
        #x,y = current
        #square = canvasMain.create_rectangle((x*10),(y*10),(x*10)+10,(y*10)+10,outline = 'red')

        if current == goal:
            break
        
        for next in World.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current      
    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = Queue()
    path.put(current)
    while current != start:
        current = came_from[current]
        path.put(current)
    return path

            


    
#================== Robots ================================
class Robot:
    def __init__(self,canvas,RobotID, x, y,size =10, speed =1.0, colour='blue'):
        self.canvas = canvasMain
        self.RobotID = RobotID
        self.colour = colour
        self.Square = canvasMain.create_rectangle(x*10,y*10,x*10 + 10,y*10+10,fill = self.colour,outline = 'White')
        self.GridLocation = (x,y)
        self.CanvasLocation  = canvasMain.coords(self.Square)
        self.path = Queue()
        self.NextTile = (0,0)
        self.HasObjective = False
        self.ObjectiveLocation = (0,0)
        self.speed = speed 
        self.size = size 
        self.vx = 0
        self.vy = 0
        self.Score = 0

    def FollowPath(self): #Robot follows the path to the treasure.

        if self.NextTile == (0,0): self.NextTile = self.path.get()

        x,y,x2,y2 = self.canvas.coords(self.Square)
        self.CanvasLocation = x,y,x2,y2

        x =x/10
        y =y/10

        if (x,y) in World.grass: #update the stored information for the grid location
            self.GridLocation = (x,y)

        if (x,y) == self.NextTile:
            if self.path.empty():
                self.vx = 0
                self.vy = 0
                self.HasObjective = False
            else:
                self.NextTile =self.path.get()
                ntx,nty = self.NextTile
                self.vx = ntx - x
                self.vy = nty - y                
  
        x = ((x *10) + (self.vx)*self.speed)
        y = ((y *10) + (self.vy)*self.speed)

        self.canvas.coords(self.Square , x, y, x + self.size, y + self.size)

    def FindNewObjective(self):
        x1,y1 = self.GridLocation
        shortestdistance = 999
        closest = 0

        
        
        for c in range (0,len(LandmarkList)):
            if (x1,y1) == LandmarkList[c].location:
                self.canvas.delete(LandmarkList[c].square)
                if  LandmarkList[c].found == False:
                    LandmarkList[c].found = True
                    self.Score += 100
                    if LandmarkList[c].Treasure == '':
                        continue
                    else:
                        TreasureList[LandmarkList[c].Treasure].Reveal(self.colour)
                        TreasureList[LandmarkList[c].Treasure].Found = True
                        self.Score += 50
                        
                
            
            if LandmarkList[c].found == True: continue
            
            distance = (LandmarkList[c].GetDistance(x1,y1))
            
            if distance < shortestdistance:
                shortestdistance = distance
                closest = c

        if shortestdistance == 999:
            x,y = randomvalidcoord()
            self.ObjectiveLocation = (x,y)
        else:
            x,y = LandmarkList[closest].location
            self.ObjectiveLocation = (x,y)

        parents = FindRobotPath(World,(x1,y1),(x,y))
        self.path = reconstruct_path(parents,(x1,y1),(x,y))
        self.path.reverse()
        
#======================== Functions ================================
    
def randomvalidcoord(): #Finds a random coordinate which can be used(not a wall)
    x1 = random.randint(1,200)
    y1 = random.randint(1,200)

    if (x1,y1) in World.grass:
        return (x1,y1) 
    else:
        return randomvalidcoord()

Map = ['Maps\MAP1 - Large.txt','Maps\MAP1 - Medium.txt','Maps\MAP1 - Small.txt']
ProjectBanner = ['Graphics\LargeBanner.gif','Graphics\LargeBanner.gif','Graphics\SmallBanner.gif']
Width =[1210,910,510]
Height =[610,510,410]
GWidth = [120,90,50]
GHeight =[60,50,40]

def getinfo(num):
    Mapc = Map[num]
    Widthc = Width[num]
    Heightc = Height[num]
    GWidthc = GWidth[num]
    GHeightc = GHeight[num]
    ProjectBannerc = ProjectBanner[num]

    return Mapc,Widthc,Heightc,GWidthc,GHeightc,ProjectBannerc

def UpdateHUD():
    for x in range (0,2):
        rlx,rly,ignore1,ignore2 = RobotList[x].CanvasLocation
        rlx,rly = rlx+5,rly+5
        tlx,tly = RobotList[x].ObjectiveLocation
        tlx,tly = (tlx*10)+5,(tly*10)+5
        canvasRobotInfo.itemconfig(RobotCordLabels[x],text = RobotList[x].GridLocation)
        canvasRobotInfo.itemconfig(RobotScoreLables[x],text = RobotList[x].Score)
        canvasMain.coords(RobotObjectiveLines[x],rlx,rly,tlx,tly)
        
#===================================================================

choice = 0 # changing between the different sized maps

Map,Width,Height,GWidth,GHeight,ProjectBanner = getinfo(choice)
             
window = Tk()

canvasMain = Canvas(window, width=Width, height=Height, bg='white')
canvasTreasures = Canvas(window, width=200, height=Height+100, bg='White')
canvasRobotInfo = Canvas(window, width=Width, height=100, bg='White')

World = squaregrid(canvasMain,GWidth,GHeight) #sg

canvasMain.grid(row = 0,column = 0)
canvasTreasures.grid(row = 0,column =1,rowspan=2)
canvasRobotInfo.grid(row = 1,column = 0)

canvasTreasures.create_rectangle(2,8,200,Height+100)
canvasRobotInfo.create_rectangle(10,2,Width,98)
canvasRobotInfo.create_text(100,25,anchor=E,text = 'Name:')
canvasRobotInfo.create_text(160,25,anchor=W,text = 'Red Bot',fill = 'Red')
canvasRobotInfo.create_text(270,25,anchor=W,text = 'Blue Bot',fill = 'Blue')
canvasRobotInfo.create_text(100,45,anchor=E,text = 'Location:')
canvasRobotInfo.create_text(100,65,anchor=E,text = 'Score:')

if choice < 2:
    canvasRobotInfo.create_image(Width -1,3,anchor = NE,image=World.LargeProjectBanner)
else:
    canvasRobotInfo.create_image(Width -1,3,anchor = NE,image=World.SmallProjectBanner)

RobotCordLabels = []
RobotCordLabels.append(canvasRobotInfo.create_text(160,45,anchor=W,text = ''))
RobotCordLabels.append(canvasRobotInfo.create_text(270,45,anchor=W,text = ''))
RobotScoreLables = []
RobotScoreLables.append(canvasRobotInfo.create_text(160,65,anchor=W,text =''))
RobotScoreLables.append(canvasRobotInfo.create_text(270,65,anchor=W,text =''))


x = 0
y = 0

with open(Map,'r') as f:
    for line in f:
        y += 1
        for character in line:
            x += 1
            if x == len(line):
                x = 0
            if character == '0': World.grass.append((x,y))
            if character == '1': World.walls.append((x,y))
            if character == '2': World.water.append((x,y))
            if character == '3': World.trees.append((x,y))

World.drawgrid()

RobotObjectiveLines = []
RobotObjectiveLines.append(canvasMain.create_line(0,0,0,0,fill = 'Red'))
RobotObjectiveLines.append(canvasMain.create_line(0,0,0,0,fill = 'Blue'))

RobotList = []
LandmarkList = []
TreasureList = []
Treasures = [['Master Sword', 'The Master Sword is a fucking cool Sword'],
             ['Jade drogon', ' A dragon which is Jade'],
             ['Really cool thing', 'This thing is really cool'],
             ['Another really cool thing','This thing is also really cool'],
             ['Reeces seal of approval','You lucky person'],
             ['FREE BEER','Its Beer. And its Free!']]


for x in range (0,14): #Creating all the Landmarks
    x1,y1 = randomvalidcoord()
    LandmarkList.append(Landmark(x,x1,y1,canvasMain))

TrA = len(Treasures)

for x in range (0,TrA): #Uses information from the Treasure list to create Treasure Objects.
    Tr = Treasures.pop(0)
    TreasureList.append(Treasure(Tr[0],Tr[1]))
    
TL = 0

while TL != TrA:
    TL = 0
    randLand= random.randint(0,len(LandmarkList)-1)
     
    if LandmarkList[randLand].Treasure == '':
        for x in range (0,len(TreasureList)):
            if TreasureList[x].used == False: 
                LandmarkList[randLand].Treasure = x
                TreasureList[x].used = True
                break
        
    for x in range (0,len(TreasureList)):
       if TreasureList[x].used == True:
           TL +=1

for x in range (0,2):
    x1,y1 = randomvalidcoord()
    Colour = 'Blue'
    if x % 2 == 0: Colour = 'Red'
    RobotList.append(Robot(canvasMain,x,x1,y1,speed = 1,size= 10,colour = Colour))

#============================== Main =================================

Running = True

while Running == True:
    for x in range (0,2): #So all actions within here are implimented for both Robots.
        
        if RobotList[x].HasObjective == False:
            RobotList[x].FindNewObjective()
            RobotList[x].HasObjective = True
    
        RobotList[x].FollowPath()
        
    UpdateHUD()
    canvasMain.update()
    time.sleep(0.01)
window.mainloop()




