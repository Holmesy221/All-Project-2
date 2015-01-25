from math import sqrt
# ================== Landmark and Treasures ========================

class Landmark():
    def __init__(self,ID,x,y,canvas):
        self.ID = ID
        self.x = x
        self.y = y
        x,y = self.x,self.y
        x=x*10
        y=y*10
        self.location = (self.x,self.y)
        self.canvas = canvas
        self.found = False
        self.square = self.canvas.create_rectangle(x,y,x+10,y+10,fill = "Dark Green",outline = 'Gold',width = 2)
        self.Treasure = ''
        
        
    def GetDistance(self,r1,r2):
        distance = sqrt(((r1-self.x)**2) + ((r2-self.y)**2))
        return distance

