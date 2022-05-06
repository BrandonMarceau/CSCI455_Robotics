import speech_recognition as sr
import time
import vlc

from Maestro import Controller


MOTORS = 1
TURN = 2
BODY = 0
HEADTURN = 3
HEADTILT = 4
ELBOW = 7
SHOULDER = 5


class VoiceController():
    def __init__(self):
        self.tango = Controller()
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.motors = 6000
        self.turn = 6000
        self.tango.setTarget(MOTORS, 6000)
        self.tango.setTarget(TURN, 6000)
        
################################
        
    def forward(self):
        print('robot forward')
        if (self.motors == 6000):
            self.motors -= 700
            print('starting')
        else:
            self.motors -= 200
            if(self.motors < 4900):
                self.motors = 4900
            print('going faster')
        self.tango.setTarget(MOTORS, self.motors)

    def backward(self):
        if(self.motors == 6000):
            self.motors += 700
        else:
            self.motors += 200
            if(self.motors  > 7100):
                self.motors = 7100
        #print(self.motors)
        self.tango.setTarget(MOTORS, self.motors)

    def left(self):
        # Motors, turn
        
        self.turn += 850
        if(self.turn > 6850):
            self.turn = 6850
        #print(self.turn)
        self.tango.setTarget(TURN, self.turn)

    def right(self):
        self.turn -= 850
        if(self.turn < 5150):
            self.turn = 5150
        #print(self.turn)
        self.tango.setTarget(TURN, self.turn)

    def stop(self):
        self.motors = 6000
        self.turn = 6000
        print(self.motors)
        self.tango.setTarget(MOTORS, self.motors)
        self.tango.setTarget(TURN, self.turn)

######################################

    def waistRight(self):            
        # Waist, turn
        self.body -= 600
        if(self.body < 3000 ):
               self.body = 3000
        #print(self.body)
        self.tango.setTarget(BODY, self.body)
            
    def waistCenter(self): 
        self.body = 6000
        self.tango.setTarget(BODY, self.body)

    def waistLeft(self):
        self.body += 600
        if(self.body > 9000):
               self.body = 9000
        #print(self.body)
        self.tango.setTarget(BODY, self.body)

#######################################

    def headDown(self):
        self.headTurn -= 400
        if(self.headTurn < 3000):
            self.headTurn = 3000
        #print(self.headTurn)
        self.tango.setTarget(HEADTURN, self.headTurn)

    def headCenter(self):
        self.headTurn = 6000
        self.headTilt = 6000
        self.tango.setTarget(HEADTILT, self.headTilt)
        self.tango.setTarget(HEADTURN, self.headTurn)

    def headUp(self):
        self.headTurn += 400
        if(self.headTurn > 9000):
            self.headTurn = 9000
        #print(self.headTurn)
        self.tango.setTarget(HEADTURN, self.headTurn)
        
    def headRight(self):
        self.headTilt -= 400
        if(self.headTilt < 3000):
            self.headTilt = 3000
        #print(self.headTilt)
        self.tango.setTarget(HEADTILT, self.headTilt)
            
    def headLeft(self):
        self.headTilt += 400
        if(self.headTilt > 9000):
            self.headTilt = 9000
        #print(self.headTilt)
        self.tango.setTarget(HEADTILT, self.headTilt)

##########################################################

    def hammerTime(self):
        self.left()
        
        p = vlc.MediaPlayer('hammertime.mp3')
#         value = 7500
        p.play()
        value = 8000
        for i in range(7):
            for i in range(5):
                self.headUp()
                self.tango.setTarget(ELBOW, value)
                time.sleep(0.1)
                value -= 400
                self.tango.setTarget(ELBOW, value)
                time.sleep(0.1)
            for i in range(5):
                self.headDown()
                value += 400
                time.sleep(0.1)
                self.tango.setTarget(ELBOW, value)
        p.stop()
        self.stop()

def main():
    
    controller = VoiceController()
    listening = True
    while listening:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 3000
            r.pause_threshold = 0.6
            r.non_speaking_duration = 0.6
            
            try:
                print("listening")
                audio = r.listen(source)            
                print("Got audio")
                word = r.recognize_google(audio)
                print(word)
                if word.lower().find('head') > -1:
                    if word.lower().find('left') > -1:
                        controller.headLeft()
                        print('head left')
                    elif word.lower().find('center') > -1:
                        controller.headCenter()
                        print('head center')
                    elif word.lower().find('right') > -1:
                        controller.headRight()
                        print('head right')
                    elif word.lower().find('down') > -1:
                        controller.headDown()
                        print('head down')
                    elif word.lower().find('up') > -1:
                        controller.headUp()
                        print('head up')
                elif word.lower().find('had') > -1:
                    if word.lower().find('left') > -1:
                        controller.headLeft()
                        print('head left')
                    elif word.lower().find('center') > -1:
                        controller.headCenter()
                        print('head center')
                    elif word.lower().find('right') > -1:
                        controller.headRight()
                        print('head right')
                    elif word.lower().find('down') > -1:
                        controller.headDown()
                        print('head down')
                    elif word.lower().find('up') > -1:
                        controller.headUp()
                        print('head up')

                        
                elif word.lower().find('waste') > -1 or word.lower().find('waist') > -1 or word.lower().find('body') > -1:
                    if word.lower().find('left') > -1:
                        controller.waistLeft()
                        print('waist left')
                    elif word.lower().find('center') > -1:
                        controller.waistCenter()
                        print('waist center')
                    elif word.lower().find('right') > -1:
                        controller.waistRight()
                        print('waist right')
                        
                elif word.lower().find('go') > -1:        
                    if word.lower().find('forward') > -1:
                        controller.forward()
                    elif word.lower().find('back') > -1:
                        controller.backward()
                        print('robot backward')
                    elif word.lower().find('left') > -1:
                        controller.left()
                        print('robot left')
                    elif word.lower().find('right') > -1:
                        controller.right()
                        print('robot right')
                elif word.lower().find('hammer') > -1:
                    controller.hammerTime()
                    print('HAMMER TIME!')
                    
                elif word.lower().find('stop') > -1:
                    controller.stop()
                    print('stop')
                else:
                    controller.stop()
                    print('stop')
                    
            except sr.UnknownValueError:
                controller.stop()
                print("Don't know that word")
            

main()
