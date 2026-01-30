"""
Behavior Challenge 2: Spin in Place (EASY - Moderate Guidance)
Rotate 360° without moving forward

INSTRUCTIONS:
- Complete the spin_right() function
- Adjust timing for full 360° rotation
"""

from machine import Pin
import time

# Setup pins (DONE FOR YOU)
fl1 = Pin(8, Pin.OUT); fl2 = Pin(9, Pin.OUT)
fr1 = Pin(11, Pin.OUT); fr2 = Pin(12, Pin.OUT)
rl1 = Pin(5, Pin.OUT); rl2 = Pin(6, Pin.OUT)
rr1 = Pin(2, Pin.OUT); rr2 = Pin(3, Pin.OUT)

def spin_right():
    """
    Spin in place (tank turn)
    Left side forward, Right side backward
    """
    # TODO: Complete this function
    # Left wheels forward: high/low
    # Right wheels backward: low/high
    pass

def stop_all():
    """Stop all motors (DONE FOR YOU)"""
    fl1.low(); fl2.low(); fr1.low(); fr2.low()
    rl1.low(); rl2.low(); rr1.low(); rr2.low()

# Main program
print("Spinning 360 degrees...")

# TODO: Call spin_right()

# TODO: Wait for full rotation (try 2.4 seconds, adjust if needed)

# TODO: Stop all motors

print("Spin complete!")
