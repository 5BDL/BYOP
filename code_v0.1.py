# B.Y.O.P - Baby Yoda Ornament Platform Project - Model Code
'''
BYOP is a project that my wife came up with based on her adoration of "The Child" 
from the new series (circa 12/2019 of the Mandalorian on Disney+).  The Child is 
basically a baby Yoda from the Star Wars world.  

The initial idea was "conceived" during the X-mas timeframe of 2019 - for reasons
that will be obvious as the requirements are described.  The original concept is 
for a baby Yoda figure to:
1. Raise its hand
2. Close its eyes (depicting the actions in the series)
3. Using the "force" start a light up sequence for an X-mas tree
    3a. "Float" a star from the ground to the top of the tree
    3b. Light the star
    3c. Light the rest of the tree

"Floating a star" was removed from the scope of the project and the sequence would follow:
    Same 1-2
    3a. Light up a path of lights to the star
    3b. Light the star
    3c. Light the rest of the tree
    4. [Stretch] Fall down from exhaustion
    
In addition to the sequence, the solution will be built as a platform that will be bluetooth
& IoT enabled.  So, basically we can initiate the "baby Yoda" force sequence and kick off
any other IoT event - turn on lights, play music, move a connected object, send a text...etc, 
basically, create an input & output event that is IoT enabled to trigger baby Yoda to do his 
force thing & send an event that can be mapped (i.e. io.adafruit or IFTTT or AWS, etc.) to 
complete an action.
'''

import array
from digitalio import DigitalInOut, Direction, Pull
import board
import pulseio
import time
import neopixel
from adafruit_motor import servo

## Hardware Configuration
# Define Servo Motor
twistpwm = pulseio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency=50)
raisepwm = pulseio.PWMOut(board.A4, duty_cycle=2 ** 15, frequency=50)
twistServo = servo.Servo(twistpwm)
raiseServo = servo.Servo(raisepwm)

# NeoPixel count - only 1 on board...need to determine IO port
NUMPIXELS = 1
#neopixels=neopixel.NeoPixel(PIN_NEOPIXEL,NUMPIXELS,brightness=0.2,auto_write=False)

## Software Configuration
# Global Variables

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
SLEEP = 6
arm_raise_sleep = .08
arm_lower_sleep = .03
arm_twistout_sleep = .1
arm_twistin_sleep = .01
start_angle = 35
angle_step_a = 6
angle_step_twistout = -3
angle_step_raise = 4
angle_step_b = -6
angle_raise = 180
angle_lower = 20
angle_twistin = 160
angle_twistout = 45
angle_left = 70
angle_right = 0

# Functions

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def raise_arm():
    for angle in range(angle_lower, angle_raise, angle_step_a):
        raiseServo.angle = angle
        time.sleep(arm_raise_sleep)
        print("Raise Angle = %0.2f" % angle)

def lower_arm():
    for angle in range(angle_raise, angle_lower, angle_step_b):
        raiseServo.angle = angle
        time.sleep(arm_lower_sleep)
        print("Lower Angle = %0.2f" % angle)

def twistout_arm():
    for angle in range(angle_twistin, angle_twistout, angle_step_twistout):
        twistServo.angle = angle
        time.sleep(arm_twistout_sleep)
        print("Twist Out Angle = %0.2f" % angle)

def twistin_arm():
    for angle in range(angle_twistout, angle_twistin, angle_step_a):
        twistServo.angle = angle
        time.sleep(arm_twistin_sleep)
        print("Twist In Angle = %0.2f" % angle)

while True:
#    neopixels.fill(RED)
#    neopixels.show()
    time.sleep(1)
    raise_arm()
    time.sleep(2)
    print("Twist Out Called")
    twistout_arm()
    time.sleep(3)
    twistin_arm()
    print("Twist In Called")
    time.sleep(.1)
    lower_arm()
    print("Lower Arm Called")
    time.sleep(2)
