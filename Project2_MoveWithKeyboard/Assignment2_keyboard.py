import tkinter as tk
from Maestro import Controller
import thread

MOTORS = 0
TURN = 1
BODY = 2
HEADTURN = 3
HEADTILT = 4

class KeyControl():
    def __init__(self,win):
        self.root = win
        self.tango = Controller()
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.motors = 6000
        self.turn = 6000
        
    def arrow(self, key):
        print(key.keycode)
        # Motors, foward and backward
        if key.keycode == 111: #up arrow
            if (self.motors == 6000):
                self.motors -= 700
            else:
                self.motors -= 200
                if(self.motors < 4900):
                    self.motors = 4900
            #print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
        if key.keycode == 116: #down arrow
            if(self.motors == 6000):
                self.motors += 700
            else:
                self.motors += 200
                if(self.motors  > 7100):
                    self.motors = 7100
            #print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)

        # Motors, turn
        if key.keycode == 113: #left arrow
            self.turn += 700
            if(self.turn > 6700):
                self.turn = 6700
            #print(self.turn)
            self.tango.setTarget(TURN, self.turn)
        if key.keycode == 114: #right arrow
            self.turn -= 700
            if(self.turn < 5300):
                self.turn = 5300
            #print(self.turn)
            self.tango.setTarget(TURN, self.turn)

        # Motors, stop
        if key.keycode == 65: #spacebar
            self.motors = 6000
            self.turn = 6000
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
            self.tango.setTarget(TURN, self.turn)

    def waist(self, key):
        print(key.keycode)            
        # Waist, turn
        if key.keycode == 52:
            self.body -= 600
            if(self.body < 3000 ):
                   self.body = 3000
            #print(self.body)
            self.tango.setTarget(BODY, self.body)
        if key.keycode == 53:
            self.body = 6000
            self.tango.setTarget(BODY, self.body)
        if key.keycode == 54:
            self.body += 600
            if(self.body > 9000):
                   self.body = 9000
            #print(self.body)
            self.tango.setTarget(BODY, self.body)

    def head(self, key):
        print(key.keycode)
        # head turn
        if key.keycode == 38:
            self.headTurn -= 400
            if(self.headTurn < 3000):
                self.headTurn = 3000
            #print(self.headTurn)
            self.tango.setTarget(HEADTURN, self.headTurn)
        if key.keycode == 39:
            self.headTurn = 6000
            self.tango.setTarget(HEADTURN, self.headTurn)
        if key.keycode == 40:
            self.headTurn += 400
            if(self.headTurn > 9000):
                self.headTurn = 9000
            #print(self.headTurn)
            self.tango.setTarget(HEADTURN, self.headTurn)
            
        # head tilt
        if key.keycode == 24:
            self.headTilt -= 400
            if(self.headTilt < 3000):
                self.headTilt = 3000
            #print(self.headTilt)
            self.tango.setTarget(HEADTILT, self.headTilt)
        if key.keycode == 25:
            self.headTilt = 6000
            self.tango.setTarget(HEADTILT, self.headTilt)
        if key.keycode == 26:
            self.headTilt += 400
            if(self.headTilt > 9000):
                self.headTilt = 9000
            #print(self.headTilt)
            self.tango.setTarget(HEADTILT, self.headTilt)


win = tk.Tk()
keys = KeyControl(win)
win.bind('<Up>', keys.arrow)
win.bind('<Down>', keys.arrow)
win.bind('<Left>', keys.arrow)
win.bind('<Right>', keys.arrow)
win.bind('<Key-space>', keys.arrow)

win.bind('<Key-z>', keys.waist)
win.bind('<Key-x>', keys.waist)
win.bind('<Key-c>', keys.waist)

win.bind('<Key-a>', keys.head)
win.bind('<Key-s>', keys.head)
win.bind('<Key-d>', keys.head)

win.bind('<Key-q>', keys.head)
win.bind('<Key-w>', keys.head)
win.bind('<Key-e>', keys.head)

win.mainloop()

