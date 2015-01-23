import random
  
#======================== Functions ================================
def randomvalidcoord(World): #Finds a random coordinate which can be used(not a wall)
    x1 = random.randint(1,200)
    y1 = random.randint(1,200)

    if (x1,y1) in World.grass:
        return (x1,y1) 
    else:
        return randomvalidcoord(World)

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

def UpdateHUD(RobotList,canvasMain,canvasRobotInfo,RobotCordLabels,RobotScoreLables,RobotObjectiveLines):
    for x in range (0,2):
        rlx,rly,ignore1,ignore2 = RobotList[x].CanvasLocation
        rlx,rly = rlx+5,rly+5
        tlx,tly = RobotList[x].ObjectiveLocation
        tlx,tly = (tlx*10)+5,(tly*10)+5
        canvasRobotInfo.itemconfig(RobotCordLabels[x],text = RobotList[x].GridLocation)
        canvasRobotInfo.itemconfig(RobotScoreLables[x],text = RobotList[x].Score)
        canvasMain.coords(RobotObjectiveLines[x],rlx,rly,tlx,tly)
