from ProgramSetup import *
from tkinter import *
from Functions import *
        
#========================= Initialisation ============================

(World,RobotList,canvasMain,
canvasRobotInfo,RobotCordLabels,
RobotScoreLables,RobotObjectiveLines,TrafficLightList) = Initialise(2)



#============================== Main =================================

Running = True

while Running == True:
    for x in range (0,10):
        rand = random.randint(0,1000)
        if rand >0 and rand <5:
            TrafficLightList[x].Switch()
        
    for x in range (0,2): #So all actions within here are implimented for both Robots
        
        if RobotList[x].HasObjective == False:
            RobotList[x].FindNewObjective()
            RobotList[x].HasObjective = True
    
        RobotList[x].FollowPath()
        
    UpdateHUD(RobotList,canvasMain,canvasRobotInfo,RobotCordLabels,RobotScoreLables,RobotObjectiveLines)
    canvasMain.update()
    time.sleep(0.01)
window.mainloop()
