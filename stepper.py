import RPi.GPIO as GPIO
import time
import keyboard
from multiprocessing import Process

class Stepper:
    def __init__(self):
        self.steppingSequence = list(range(0,8))
        self.steppingSequence[0] = [0,1,0,0]
        self.steppingSequence[1] = [0,1,0,1]
        self.steppingSequence[2] = [0,0,0,1]
        self.steppingSequence[3] = [1,0,0,1]
        self.steppingSequence[4] = [1,0,0,0]
        self.steppingSequence[5] = [1,0,1,0]
        self.steppingSequence[6] = [0,0,1,0]
        self.steppingSequence[7] = [0,1,1,0]
        self.motor1 = [24, 4, 23, 25]
        self.motor2 = [18, 22, 17, 27]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        list(map(lambda x: GPIO.setup(x, GPIO.OUT), self.motor1))
        list(map(lambda x: GPIO.setup(x, GPIO.OUT), self.motor2))

    def setMotor1(self, state):
        list(map(lambda x,y: GPIO.output(x,y), self.motor1, state ))

    def setMotor2(self, state):
        list(map(lambda x,y: GPIO.output(x,y), self.motor2, state ))

    def rotate1(self, steps, orientation = 'clockwise', delay=0.68):
        if orientation == 'clockwise':    
            for step in range(steps):
                for sequence in self.steppingSequence:
                    self.setMotor1(sequence)
                    time.sleep(delay/1000.0)
        else:
            for step in range(steps):
                for sequence in reversed(self.steppingSequence):
                    self.setMotor1(sequence)
                    time.sleep(delay/1000.0)
        self.setMotor1([0,0,0,0])

    def rotate2(self, steps, orientation = 'clockwise', delay=0.68):
        if orientation == 'clockwise':    
            for step in range(steps):
                for sequence in self.steppingSequence:
                    self.setMotor2(sequence)
                    time.sleep(delay/1000.0)
        else:
            for step in range(steps):
                for sequence in reversed(self.steppingSequence):
                    self.setMotor2(sequence)
                    time.sleep(delay/1000.0)
        self.setMotor2([0,0,0,0])

stepper = Stepper()
#stepper.rotate1(int(360/5.625*64/8), 0.68)

def right(e):
    if keyboard.is_pressed("right"):
        thread = Process(target=stepper.rotate1(int(64/8)))
        thread.start()
        
def left(e):
    if keyboard.is_pressed("left"):
        thread = Process(stepper.rotate1(int(64/8), orientation='counter-clockwise'))
        thread.start()

def up(e):
    if keyboard.is_pressed("up"):
        thread = Process(stepper.rotate2(int(64/8)))
        thread.start()
def down(e):
    if keyboard.is_pressed("down"):
        thread = Process(stepper.rotate2(int(64/8), orientation='counter-clockwise'))
        thread.start()

keyboard.on_press_key("left", left)
keyboard.on_press_key("right", right)
keyboard.on_press_key("up", up)
keyboard.on_press_key("down", down)
#Use ctrl+c to stop
while True:
    pass