from tkinter import *
import collections, random, time, sys
from math import sqrt
from Queues import *
from Worlds import *
from Treasures import *
from Landmarks import *
from Robots import *
from Functions import *
from ProgramSetup import *

def Initialise(Size, AOR = 2, AOL = 14, AOT = 4):
    
    choice = Size # changing between the different sized maps

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
        x1,y1 = randomvalidcoord(World)
        LandmarkList.append(Landmark(x,x1,y1,canvasMain))

    TrA = len(Treasures)

    for x in range (0,TrA): #Uses information from the Treasure list to create Treasure Objects.
        Tr = Treasures.pop(0)
        TreasureList.append(Treasure(Tr[0],Tr[1],TreasureList,canvasTreasures))
        
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
        x1,y1 = randomvalidcoord(World)
        Colour = 'Blue'
        if x % 2 == 0: Colour = 'Red'
        RobotList.append(Robot(canvasMain,x,x1,y1,LandmarkList,TreasureList,World,speed = 1,size= 10,colour = Colour))

    return RobotList,canvasMain,canvasRobotInfo,RobotCordLabels,RobotScoreLables,RobotObjectiveLines
