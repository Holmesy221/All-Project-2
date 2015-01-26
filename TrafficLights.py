from tkinter import *
class TrafficLight():
    def __init__(self, canvas, Location):
        self.Location = Location
        self.canvas = canvas
        self.onoff = 'off'
        self.TrafficOpenImage = PhotoImage(file = 'Graphics\TrafficOpen.Gif')
        self.TrafficClosedImage = PhotoImage(file = 'Graphics\TrafficClosed.Gif')
        self.TLImage = self.canvas.create_image(self.Location,anchor = "nw", image = self.TrafficOpenImage)

    def Switch(self):
        self.canvas.delete(self.TLImage)
        
        if self.onoff =='on':
            self.TLImage=self.canvas.create_image(self.Location,anchor = 'nw', image = self.TrafficClosedImage)
            self.onoff='off'
        else:
            self.TLImage=self.canvas.create_image(self.Location,anchor = "nw", image = self.TrafficOpenImage)
            self.onoff='on'
