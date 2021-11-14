import turtle as tt
import numpy as np
from time import sleep



class prop():
    def __init__(self):
        self.velocity = np.array([50.0,0.0])
        self.abs_v = 10.0
        self.loc = np.array([0.0,150.0])
        self.force = 0.0
        self.distance = 300.0

    def setini(self, x, y, vx, vy, g):
        self.velocity = np.array([vx, vy])
        self.loc = np.array([x,y])
        self.g = -1 * g
    
    def run(self):
        self.distance = self.loc[0] ** 2 + self.loc[1] ** 2
        self.force = self.g / self.distance
        self.velocity += self.force * self.loc
        self.loc += self.velocity * 0.1
        self.abs_v = np.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)


sun = tt.Turtle()
sun.color('red')
sun.turtlesize(1)
sun.shape('circle')


t = tt.Turtle()
tt.screensize(1000,1000,'white')
t.pensize(2)
t.turtlesize(0.5)
t.color('purple')
t.shape('circle')
'''t.goto(-5,-5)
t.goto(-5,5)
t.goto(5,5)
t.goto(5,-5)
t.goto(-5,-5)'''
t.penup()
#t.hideturtle()
tp = prop()
#tp.setini(0.0, 300.0, 50.0, -80.0, 980)
tp.setini(100.0, 0.0, 0.0, 100.0, 1000.0)      #circular orbit
t.goto(tp.loc)
t.pendown()

t2 = tt.Turtle()
t2.pensize(2)
t2.turtlesize(0.5)
t2.shape('circle')
t2.color('blue')
t2.penup()
#t2.hideturtle()
tp2 = prop()
tp2.setini(0.0, -150.0, -50.0, 140.0, 1500)
t2.goto(tp2.loc)
t2.pendown()

t3 = tt.Turtle()
t3.pensize(2)
t3.turtlesize(0.5)
t3.shape('circle')
t3.color('green')
t3.penup()
#t3.hideturtle()
tp3 = prop()
tp3.setini(200.0, 0.0, 0.0, 10.0, 300)
t3.goto(tp3.loc)
t3.pendown()

t4 = tt.Turtle()
t4.pensize(2)
t4.turtlesize(0.5)
t4.shape('circle')
t4.color('orange')
t4.penup()
#t4.hideturtle()
tp4 = prop()
tp4.setini(-400.0, 0.0, 0.0, -90.0, 10000)
t4.goto(tp4.loc)
t4.pendown()


print('start')
i = 0
sleepr = 0.2
while tp.distance > 10:
    '''i += 1
    if i % 400 == 0:
        tt.clearscreen()
        t.penup()
        t.goto(tp.loc)
        t.pendown()
        t2.penup()
        t2.goto(tp2.loc)
        t2.pendown()
        t3.penup()
        t3.goto(tp3.loc)
        t3.pendown()
        t4.penup()
        t4.goto(tp4.loc)
        t4.pendown()'''

    tp.run()
    t.goto(tp.loc)
    #sleep(sleepr / tp.abs_v)
    #print(tp.loc)
    tp2.run()
    t2.goto(tp2.loc)
    #sleep(sleepr / tp2.abs_v)
    tp3.run()
    t3.goto(tp3.loc)
    #sleep(sleepr / tp3.abs_v)
    tp4.run()
    t4.goto(tp4.loc)
    #sleep(sleepr / tp4.abs_v)
    



