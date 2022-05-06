import speech_recognition as sr
import pyttsx3
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


class Control():
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

    def forward(self, speed, seconds):
        print('robot forward')
        set_speed = 600 + (speed * 100)
        self.motors -= set_speed
        self.tango.setTarget(MOTORS, self.motors)
        time.sleep(seconds)
        self.motors = 6000
        self.tango.setTarget(MOTORS, self.motors)
        time.sleep(2)

    def backward(self, speed, seconds):
        print('robot backwards')
        set_speed = 600 + (speed * 100)
        self.motors += set_speed
        self.tango.setTarget(MOTORS, self.motors)
        time.sleep(seconds)
        self.motors = 6000
        self.tango.setTarget(MOTORS, self.motors)
        time.sleep(2)

    def left(self, seconds):
        print("robot left")
        self.turn += 950
        self.tango.setTarget(TURN, self.turn)
        time.sleep(seconds)
        self.turn = 6000
        self.tango.setTarget(TURN, self.turn)
        time.sleep(2)

    def right(self, seconds):
        print('robot right')
        self.turn -= 850
        self.tango.setTarget(TURN, self.turn)
        time.sleep(seconds)
        self.turn = 6000
        self.tango.setTarget(TURN, self.turn)
        time.sleep(2)

    def stop(self):
        self.motors = 6000
        self.turn = 6000
        print(self.motors)
        self.tango.setTarget(MOTORS, self.motors)
        self.tango.setTarget(TURN, self.turn)

    ######################################

    def waistRight(self, degrees):
        print("turn waist right")
        set_waist = degrees * 30
        self.body -= set_waist
        self.tango.setTarget(BODY, self.body)
        time.sleep(2)

    def waistLeft(self, degrees):
        print("turn waist left")
        set_waist = degrees * 30
        self.body += set_waist
        self.tango.setTarget(BODY, self.body)
        time.sleep(2)

    #######################################

    def headDown(self, degrees):
        print("head up")
        set_head_tilt = degrees * 60
        self.headTurn -= set_head_tilt
        self.tango.setTarget(HEADTURN, self.headTurn)
        time.sleep(2)

    def headUp(self, degrees):
        print("head down")
        set_head_tilt = degrees * 60
        self.headTurn += set_head_tilt
        self.tango.setTarget(HEADTURN, self.headTurn)
        time.sleep(2)

    def headRight(self, degrees):
        print("head right")
        set_head_turn = degrees * 60
        self.headTilt -= set_head_turn
        self.tango.setTarget(HEADTILT, self.headTilt)
        time.sleep(2)

    def headLeft(self, degrees):
        print("head left")
        set_head_turn = degrees * 60
        self.headTilt += set_head_turn
        self.tango.setTarget(HEADTILT, self.headTilt)
        time.sleep(2)

    def waitWithSeconds(self, seconds):
        print("waiting " + str(seconds) + " seconds")
        time.sleep(seconds)

    def reset(self):
        self.tango.setTarget(HEADTILT, 6000)
        self.tango.setTarget(HEADTURN, 6000)
        self.tango.setTarget(BODY, 6000)
        self.tango.setTarget(MOTORS, 6000)
        self.tango.setTarget(TURN, 6000)

    def waitWithSpeech(self, userString):
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
                    if word.lower().find(userString) > -1:
                        break;
                except sr.UnknownValueError:
                    print("Don't know that word")

    def say(self, text_to_say):
        engine = pyttsx3.init()
        engine.say(text_to_say)
        engine.runAndWait()



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


