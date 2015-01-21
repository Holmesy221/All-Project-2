class Treasure():
    def __init__(self,name,desc):
        self.name = name
        self.desc = desc
        self.used = False
        self.Found = False

    def Reveal(self,colour):

        AF = 1
        
        for x in range (0,len(TreasureList)):
           if TreasureList[x].Found == True:
               AF +=1
        
        canvasTreasures.create_text(20,20*AF,anchor=W,text = self.name, fill = colour)
