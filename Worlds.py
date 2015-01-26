from tkinter import *
#=================== The World Generation =====================    
class squaregrid:
    def __init__ (self,canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.walls = []
        self.wallimage = PhotoImage(file = 'Graphics\Wall.gif')
        self.trees = []
        self.treeimage = PhotoImage(file = 'Graphics\Tree.gif')
        self.grass = []
        self.grassimage = PhotoImage(file = 'Graphics\Grass.gif')
        self.water = []
        self.TrafficLights = []
       
        
        self.LargeProjectBanner = PhotoImage(file = 'Graphics\LargeBanner.gif')
        self.SmallProjectBanner = PhotoImage(file = 'Graphics\SmallBanner.gif')

    def drawgrid(self):
        for y in range(self.height+1):
            for x in range(self.width+1):
                TType = self.draw_tile((x,y))
                self.drawtile((x,y),TType)

    def drawtile(self,gridid,TType):
        x,y = gridid
        x = x*10
        y = y*10

        if TType == 'Tree Tile': self.canvas.create_image(x,y,anchor="nw",image=self.treeimage)
        if TType == 'Wall Tile': self.canvas.create_image(x,y,anchor="nw",image=self.wallimage)
        if TType == 'Grass Tile': self.canvas.create_rectangle(x,y,x+10,y+10,outline = 'lime green',fill= 'forest green')
        if TType == 'Water Tile': self.canvas.create_rectangle(x,y,x+10,y+10,outline = 'sky blue',fill= 'light sea green')

    def draw_tile(self,gridid):

        r = ''
    
        if gridid in self.walls: r = 'Wall Tile'
        if gridid in self.trees: r = 'Tree Tile'
        if gridid in self.grass: r = 'Grass Tile'
        if gridid in self.water: r = 'Water Tile'
    
        return r

    def neighbors(self,gridid):
        (x,y) = gridid
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.passable,results)
        results = filter(self.in_bounds,results)
        return results

    def passable(self, gridid):
       return gridid not in self.walls and gridid not in self.trees and gridid not in self.water and gridid not in self.TrafficLights

    def in_bounds(self, gridid):
        (x, y) = gridid
        return 0 <= x < self.width and 0 <= y < self.height

