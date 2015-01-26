from Queues import *
from Functions import *
#================== Robots ================================
class Robot:
    def __init__(self,canvas,RobotID, x, y,LandmarkList,TreasureList,World,size =10, speed =1.0, colour='blue'):
        self.canvas = canvas
        self.RobotID = RobotID
        self.colour = colour
        self.Square = self.canvas.create_rectangle(x*10,y*10,x*10 + 10,y*10+10,fill = self.colour,outline = 'White')
        self.GridLocation = (x,y)
        self.CanvasLocation  = self.canvas.coords(self.Square)
        self.path = Queue()
        self.NextTile = (0,0)
        self.HasObjective = False
        self.ObjectiveLocation = (0,0)
        self.speed = speed 
        self.size = size 
        self.vx = 0
        self.vy = 0
        self.Score = 0
        self.LandmarkList = LandmarkList
        self.World = World
        self.TreasureList = TreasureList

    #================= Search Algorithm

    def FindRobotPath(self,startpoint,goal):
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
            
            for next in self.World.neighbors(current):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current      
        return came_from

    def reconstruct_path(self,came_from, start, goal):
        current = goal
        path = Queue()
        path.put(current)
        while current != start:
            current = came_from[current]
            path.put(current)
        return path

    #=================================

    def FollowPath(self): #Robot follows the path to the treasure.

        if self.NextTile == (0,0): self.NextTile = self.path.get()

        x,y,x2,y2 = self.canvas.coords(self.Square)
        self.CanvasLocation = x,y,x2,y2

        x =x/10
        y =y/10

        if (x,y) in self.World.grass: #update the stored information for the grid location
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

        
        
        for c in range (0,len(self.LandmarkList)):
            if (x1,y1) == self.LandmarkList[c].location:
                self.canvas.itemconfig(self.LandmarkList[c].square,outline = 'White')
                if  self.LandmarkList[c].found == False:
                    self.LandmarkList[c].found = True
                    self.Score += 100
                    if self.LandmarkList[c].Treasure == '':
                        continue
                    else:
                        self.canvas.itemconfig(self.LandmarkList[c].square,fill = self.colour)
                        self.TreasureList[self.LandmarkList[c].Treasure].Reveal(self.colour)
                        self.TreasureList[self.LandmarkList[c].Treasure].Found = True
                        self.Score += 50
    
            if self.LandmarkList[c].found == True: continue
            
            distance = (self.LandmarkList[c].GetDistance(x1,y1))
            
            if distance < shortestdistance:
                shortestdistance = distance
                closest = c

        if shortestdistance == 999:
            x,y = randomvalidcoord(self.World)
            self.ObjectiveLocation = (x,y)
        else:
            x,y = self.LandmarkList[closest].location
            self.ObjectiveLocation = (x,y)

        parents = self.FindRobotPath((x1,y1),(x,y))
        self.path = self.reconstruct_path(parents,(x1,y1),(x,y))
        self.path.reverse()
