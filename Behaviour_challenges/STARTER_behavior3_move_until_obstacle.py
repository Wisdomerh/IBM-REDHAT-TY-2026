"""
Behavior Challenge 3: Move Until Obstacle (MEDIUM)
Go forward, stop when object < 15cm detected

INSTRUCTIONS:
- Complete all the function definitions
- Main program structure is provided
- You need to write the motor control and sensor code
"""

from machine import Pin, time_pulse_us
import time

# TODO: Setup motor pins (8 pins total)
# Front left: 8, 9
# Front right: 11, 12
# Rear left: 5, 6
# Rear right: 2, 3

# TODO: Setup ultrasonic sensor pins
# Trig: Pin 14, OUTPUT
# Echo: Pin 15, INPUT

def forward():
    """Move all wheels forward"""
    # TODO: Complete this function
    pass

def stop_all():
    """Stop all motors"""
    # TODO: Complete this function
    pass

def get_distance():
    """
    Get distance from ultrasonic sensor in cm
    Return: distance in cm, or 999 if measurement fails
    """
    # TODO: Complete this function
    # Steps:
    # 1. Trigger pulse (low, high for 10us, low)
    # 2. Measure echo pulse time
    # 3. Calculate distance: (pulse_time / 2) / 29.1
    # 4. Return distance
    pass

# Main program (STRUCTURE PROVIDED)
print("Moving forward until obstacle detected...")

# TODO: Start moving forward

while True:
    # TODO: Get distance from sensor
    dist = 0  # Replace with actual distance
    
    print(f"Distance: {dist:.1f} cm")
    
    # TODO: If distance < 15cm, stop and break
    
    time.sleep(0.1)  # Check every 100ms

print("Program complete!")
