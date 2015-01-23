from tkinter import *
class Treasure():
    def __init__(self,name,desc,TreasureList,canvas):
        self.name = name
        self.desc = desc
        self.used = False
        self.Found = False
        self.TreasureList = TreasureList
        self.canvas = canvas

    def Reveal(self,colour):

        AF = 1
        
        for x in range (0,len(self.TreasureList)):
           if self.TreasureList[x].Found == True:
               AF +=1
        
        self.canvas.create_text(20,20*AF,anchor = W,text = self.name, fill = colour)
