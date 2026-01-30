"""
Behavior Challenge 4: Figure-8 Pattern (MEDIUM)
Program smooth figure-8 movement

INSTRUCTIONS:
- Define motor control functions
- Use one-sided driving to make circles
- Complete the main program to execute figure-8
"""

from machine import Pin
import time

# TODO: Setup all 8 motor pins

def forward():
    """Move forward (all wheels)"""
    pass

def circle_left():
    """
    Circle left by turning off left motors
    Only right side moves forward
    """
    pass

def circle_right():
    """
    Circle right by turning off right motors
    Only left side moves forward
    """
    pass

def stop_all():
    """Stop all motors"""
    pass

# Main program
print("Starting figure-8 pattern...")

# TODO: First circle (left) - run for ~4 seconds
# TODO: Move forward briefly to transition
# TODO: Second circle (right) - run for ~4 seconds
# TODO: Stop

print("Figure-8 complete!")
