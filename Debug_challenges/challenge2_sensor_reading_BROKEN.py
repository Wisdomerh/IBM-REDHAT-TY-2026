"""
Challenge 2: Sensor Reading (MEDIUM)
This code should read distance every second.
Find and fix the bugs!
"""

from machine import Pin, time_pulse_us
import time

trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.OUT)

def get_distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    pulse_time = time_pulse_us(echo, 1, 30000)
    distance = (pulse_time * 2) / 29.1
    return distance

while True:
    dist = get_distance()
    print("Distance:", distance, "cm")
    time.sleep(1)
