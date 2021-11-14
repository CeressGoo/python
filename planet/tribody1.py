import numpy as np
import turtle as tt

class planet():
    def __init__(self):
        self.tt = tt.Turtle()
        self.loc = [100.0,100.0]
        self.vel = [10.0, 10.0]
        self.acc = [0.0,0.0]
        self.force = 100.0
        self.m = 500.0

    def set_appr(self, color='red', shape='circle', pensize=2):
        self.tt.color(color)
        self.tt.shape(shape)
        self.tt.pensize(pensize)

    def setini(self, x:float, y:float, vx:float, vy:float, m:float):
        self.loc = [x,y]
        self.vel = [vx, vy]
        self.m = m

    def run(self):
        self.dist = np.sqrt(self.loc[0] ** 2 + self.loc[1] ** 2)
        self.force = self.grav / (self.dist ** 2)
        self.acc = 
    