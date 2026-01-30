"""
Challenge 3: Square Pattern (HARD)
This code should make the robot drive in a square.
Find and fix ALL the bugs!
"""

from machine import Pin
import time

# Setup pins (abbreviated for space)
fl1 = Pin(8, Pin.OUT); fl2 = Pin(9, Pin.OUT)
fr1 = Pin(11, Pin.OUT); fr2 = Pin(12, Pin.OUT)
rl1 = Pin(5, Pin.OUT); rl2 = Pin(6, Pin.OUT)
rr1 = Pin(2, Pin.OUT); rr2 = Pin(3, Pin.OUT)

def forward():
    fl1.high(); fl2.low(); fr1.high(); fr2.low()
    rl1.high(); rl2.low(); rr1.high(); rr2.low()

def turn_right():
    fl1.high(); fl2.low(); fr1.low(); fr2.high()
    rl1.high(); rl2.low(); rr1.low(); rr2.high()

# Drive in square
for i in range(3):  # BUG: Should be range(4) for 4 sides of a square
    forward()
    time.sleep(2)
    turn_right  # BUG: Missing () - should be turn_right()
    time.sleep(0.5)
