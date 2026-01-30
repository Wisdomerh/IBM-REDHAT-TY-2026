"""
Challenge 1: Motor Test (EASY)
This code should spin all 4 wheels forward for 2 seconds.
Find and fix the bugs!
"""

from machine import Pin
import time

# Front wheels
front_left_1 = Pin(8, Pin.OUT)
front_left_2 = Pin(9, Pin.OUT)
front_right_1 = Pin(11, Pin.OUT)
front_right_2 = Pin(12, Pin.OUT)

# Rear wheels
rear_left_1 = Pin(5, Pin.OUT)
rear_left_2 = Pin(6, Pin.OUT)
rear_right_1 = Pin(2, Pin.OUT)
rear_right_2 = Pin(3, Pin.OUT)

# Spin all wheels forward
def spin_forward()
front_left_1.high(); front_left_2.low()
front_right_1.high(); front_right_2.low()
rear_left_1.high(); rear_left_2.low()
rear_right_1.high(); rear_right_2.low()

spin_forward()
time.sleep(2)
