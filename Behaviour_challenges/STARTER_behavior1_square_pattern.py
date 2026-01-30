"""
Behavior Challenge 1: Square Pattern (EASY - Guided)
Drive in a perfect square (4 sides, 90° turns)

INSTRUCTIONS:
- Fill in the missing code where you see # TODO
- Test after each step
"""

from machine import Pin
import time

# Setup pins (DONE FOR YOU)
fl1 = Pin(8, Pin.OUT); fl2 = Pin(9, Pin.OUT)
fr1 = Pin(11, Pin.OUT); fr2 = Pin(12, Pin.OUT)
rl1 = Pin(5, Pin.OUT); rl2 = Pin(6, Pin.OUT)
rr1 = Pin(2, Pin.OUT); rr2 = Pin(3, Pin.OUT)

def forward():
    """Move forward - COMPLETE THIS"""
    # TODO: Set all wheels to spin forward
    # Hint: Left side high/low, Right side high/low
    fl1.high(); fl2.low()
    fr1.high(); fr2.low()
    # TODO: Complete for rear wheels
    pass  # Remove this line when done

def turn_right():
    """Turn right (tank turn) - COMPLETE THIS"""
    # TODO: Left side forward, Right side backward
    # Hint: Left high/low, Right low/high
    pass

def stop_all():
    """Stop all motors (DONE FOR YOU)"""
    fl1.low(); fl2.low(); fr1.low(); fr2.low()
    rl1.low(); rl2.low(); rr1.low(); rr2.low()

# Drive in square pattern
print("Starting square pattern...")

# TODO: Use a for loop to repeat 4 times (4 sides of square)
# for i in range(?):  # How many sides in a square?
    # TODO: Move forward
    # TODO: Wait 2 seconds
    # TODO: Stop
    # TODO: Wait 0.2 seconds
    # TODO: Turn right
    # TODO: Wait 0.6 seconds (for 90° turn)
    # TODO: Stop
    # TODO: Wait 0.2 seconds

print("Square complete!")
