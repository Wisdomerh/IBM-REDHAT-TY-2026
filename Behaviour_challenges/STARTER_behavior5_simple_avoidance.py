"""
Behavior Challenge 5: Simple Obstacle Avoidance (HARD)
Drive forward, backup & turn when obstacle detected

REQUIREMENTS:
- Move forward continuously
- Check for obstacles using ultrasonic sensor
- When obstacle < 20cm:
  1. Stop
  2. Backup for 0.6 seconds
  3. Turn right 90 degrees
  4. Continue forward
- Loop forever

HINTS:
- You'll need: forward(), backward(), turn_right(), stop_all()
- You'll need: get_distance() function
- Use a while True loop
- Check distance every 0.1 seconds

Write all the code yourself!
"""

from machine import Pin, time_pulse_us
import time

# Write your code here!
