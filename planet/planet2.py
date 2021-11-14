import turtle as tt
import numpy as np
#from time import sleep



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

xlib = 50 + 300 * np.random.ranf(4)
ylib = 50 + 300 * np.random.ranf(4)
vxlib = -200 + 400 * np.random.ranf(4)
vylib = -200 + 400 * np.random.ranf(4)
glib = 500 + 9000 * np.random.ranf(4)

sun = tt.Turtle()
sun.color('red')
sun.shape('circle')
sun.pensize(2)

t = tt.Turtle()
tt.screensize(1000,1000,'white')
t.pensize(2)
t.color('purple')
'''t.goto(-5,-5)
t.goto(-5,5)
t.goto(5,5)
t.goto(5,-5)
t.goto(-5,-5)'''
t.penup()
t.shape('circle')
t.turtlesize(0.5)
#t.hideturtle()
tp = prop()
tp.setini(xlib[0], ylib[0], vxlib[0], vylib[0], glib[0])
#tp.setini(100.0, 0.0, 0.0, 100.0, 1000.0)      #circular orbit
t.goto(tp.loc)
t.pendown()

t2 = tt.Turtle()
t2.pensize(2)
t2.color('blue')
t2.penup()
t2.shape('circle')
t2.turtlesize(0.5)
#t2.hideturtle()
tp2 = prop()
tp2.setini(xlib[1], ylib[1], vxlib[1], vylib[1], glib[1])
t2.goto(tp2.loc)
t2.pendown()

t3 = tt.Turtle()
t3.pensize(2)
t3.color('green')
t3.penup()
t3.shape('circle')
t3.turtlesize(0.5)
#t3.hideturtle()
tp3 = prop()
tp3.setini(xlib[2], ylib[2], vxlib[2], vylib[2], glib[2])
t3.goto(tp3.loc)
t3.pendown()

t4 = tt.Turtle()
t4.pensize(2)
t4.color('orange')
t4.penup()
t4.shape('circle')
t4.turtlesize(0.5)
#t4.hideturtle()
tp4 = prop()
tp4.setini(xlib[3], ylib[3], vxlib[3], vylib[3], glib[3])
t4.goto(tp4.loc)
t4.pendown()


print('start')
i = 0
sleepr = 0.2
while np.max([tp.abs_v, tp2.abs_v, tp3.abs_v, tp4.abs_v]) < 1000:
    i += 1
    if i % 1000 == 0:
        t.clear()
        t2.clear()
        t3.clear()
        t4.clear()
        '''t.penup()
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
    #print(f'Speed {i}: ', [tp.abs_v, tp2.abs_v, tp3.abs_v, tp4.abs_v])


    



