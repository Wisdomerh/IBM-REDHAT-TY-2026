"""
Freenove 4WD Robot with Automatic Obstacle Avoidance
------------------------------------------------------
Automatically detects obstacles, stops, backs up, turns 180°, and avoids them.
Controlled via WiFi using the Freenove app.

NOTE: Motors use DIRECTION CONTROL ONLY (no PWM speed control)
      Enable pins are not wired, so motors run at full speed when ON.
      Values represent direction: positive = forward, negative = backward

Features:
- Tank turn steering
- Ultrasonic distance sensing
- Automatic obstacle avoidance
- WiFi control interface
"""

from machine import Pin
import network
import socket
import time
import _thread
import random


# ==============================================================================
# PIN ASSIGNMENTS
# ==============================================================================

# Front wheels (direction pins only - no enable pins wired)
FRONT_LEFT_IN1 = Pin(8, Pin.OUT)
FRONT_LEFT_IN2 = Pin(9, Pin.OUT)
FRONT_RIGHT_IN3 = Pin(11, Pin.OUT)
FRONT_RIGHT_IN4 = Pin(12, Pin.OUT)

# Rear wheels (direction pins only - no enable pins wired)
REAR_LEFT_IN1 = Pin(5, Pin.OUT)
REAR_LEFT_IN2 = Pin(6, Pin.OUT)
REAR_RIGHT_IN3 = Pin(2, Pin.OUT)
REAR_RIGHT_IN4 = Pin(3, Pin.OUT)

# Sensors
TRIG_PIN = Pin(14, Pin.OUT)
ECHO_PIN = Pin(15, Pin.IN)
LED = Pin("LED", Pin.OUT)


# ==============================================================================
# CONFIGURATION SETTINGS
# ==============================================================================

# Motor control thresholds (values represent direction, not speed)
DEADZONE = 15                    # Ignore joystick inputs below this value
TANK_ENTER_THRESHOLD = 25        # Threshold to enter tank turn mode
TANK_EXIT_THRESHOLD = 40         # Threshold to exit tank turn mode
AUTO_STOP_TIMEOUT = 800          # Stop motors after 800ms of no commands
MIN_COMMAND_SPEED = 20           # Minimum value to activate motors

# Obstacle avoidance settings
OBSTACLE_DETECT_CM = 20          # Start avoiding at this distance (cm)
OBSTACLE_CRITICAL_CM = 10        # Emergency stop at this distance (cm)
AVOID_BACKUP_MS = 600            # Back up duration (milliseconds)
AVOID_TURN_MS = 1200             # Turn duration (milliseconds) - approximately 180°
SONAR_CHECK_INTERVAL = 200       # Check distance every 200ms

# Direction change cooldown
DIRECTION_CHANGE_COOLDOWN = 1000 # Don't check obstacles for 1s after direction change


# ==============================================================================
# GLOBAL STATE VARIABLES
# ==============================================================================

# Motor direction values (-100 to 100)
# NOTE: These represent DIRECTION only, not speed
# Positive = forward, Negative = backward, 0 = stop
current_left_speed = 0
current_right_speed = 0

# Timing
last_command_time = 0
last_sonar_check = 0
last_direction_change = 0

# Thread safety
command_lock = _thread.allocate_lock()

# Tank turn state
in_tank_turn = False
tank_turn_direction = None  # 'LEFT' or 'RIGHT'

# Sensor state
last_distance = 0

# Avoidance state
avoiding_obstacle = False
user_control_disabled = False


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def apply_deadzone(value):
    """
    Apply deadzone to joystick input.
    Values within the deadzone are treated as zero.
    
    Args:
        value: Input value from joystick
        
    Returns:
        0 if within deadzone, otherwise the original value
    """
    if abs(value) < DEADZONE:
        return 0
    return value


def clamp(value, min_val=-100, max_val=100):
    """
    Clamp a value between minimum and maximum bounds.
    
    Args:
        value: Value to clamp
        min_val: Minimum allowed value (default: -100)
        max_val: Maximum allowed value (default: 100)
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


# ==============================================================================
# MOTOR CONTROL
# ==============================================================================

def set_motors_direct(left_direction, right_direction):
    """
    Set motor directions.
    
    NOTE: Motors run at FULL SPEED when activated (enable pins not wired).
          This function only controls DIRECTION, not speed.
    
    Args:
        left_direction: Left side direction (-100 to 100)
                       Positive = forward, Negative = backward, 0 = stop
        right_direction: Right side direction (-100 to 100)
                        Positive = forward, Negative = backward, 0 = stop
    """
    # Left side motors
    if left_direction > 10:
        # Forward (full speed)
        FRONT_LEFT_IN1.high()
        FRONT_LEFT_IN2.low()
        REAR_LEFT_IN1.high()
        REAR_LEFT_IN2.low()
    elif left_direction < -10:
        # Backward (full speed)
        FRONT_LEFT_IN1.low()
        FRONT_LEFT_IN2.high()
        REAR_LEFT_IN1.low()
        REAR_LEFT_IN2.high()
    else:
        # Stop
        FRONT_LEFT_IN1.low()
        FRONT_LEFT_IN2.low()
        REAR_LEFT_IN1.low()
        REAR_LEFT_IN2.low()
    
    # Right side motors
    if right_direction > 10:
        # Forward (full speed)
        FRONT_RIGHT_IN3.high()
        FRONT_RIGHT_IN4.low()
        REAR_RIGHT_IN3.high()
        REAR_RIGHT_IN4.low()
    elif right_direction < -10:
        # Backward (full speed)
        FRONT_RIGHT_IN3.low()
        FRONT_RIGHT_IN4.high()
        REAR_RIGHT_IN3.low()
        REAR_RIGHT_IN4.high()
    else:
        # Stop
        FRONT_RIGHT_IN3.low()
        FRONT_RIGHT_IN4.low()
        REAR_RIGHT_IN3.low()
        REAR_RIGHT_IN4.low()


def stop_all():
    """Stop all motors immediately."""
    FRONT_LEFT_IN1.low()
    FRONT_LEFT_IN2.low()
    FRONT_RIGHT_IN3.low()
    FRONT_RIGHT_IN4.low()
    REAR_LEFT_IN1.low()
    REAR_LEFT_IN2.low()
    REAR_RIGHT_IN3.low()
    REAR_RIGHT_IN4.low()


def motor_watchdog():
    """
    Motor watchdog thread.
    Monitors motor commands and automatically stops motors if no commands
    received within the timeout period.
    """
    global current_left_speed, current_right_speed, last_command_time
    global in_tank_turn, tank_turn_direction, user_control_disabled, avoiding_obstacle
    
    while True:
        time.sleep_ms(50)
        
        with command_lock:
            # Don't apply user commands if avoiding obstacle
            if user_control_disabled or avoiding_obstacle:
                continue
            
            # Check time since last command
            time_since_last = time.ticks_diff(time.ticks_ms(), last_command_time)
            
            if time_since_last > AUTO_STOP_TIMEOUT:
                # Timeout - stop motors
                if current_left_speed != 0 or current_right_speed != 0:
                    current_left_speed = 0
                    current_right_speed = 0
                    in_tank_turn = False
                    tank_turn_direction = None
                    set_motors_direct(0, 0)
            else:
                # Apply current motor directions
                set_motors_direct(current_left_speed, current_right_speed)


# Start motor watchdog thread
_thread.start_new_thread(motor_watchdog, ())


# ==============================================================================
# ULTRASONIC SENSOR
# ==============================================================================

def get_distance_raw():
    """
    Get raw distance measurement from ultrasonic sensor.
    
    Returns:
        Distance in centimeters, or -1 if measurement failed
    """
    try:
        # Send trigger pulse
        TRIG_PIN.low()
        time.sleep_us(2)
        TRIG_PIN.high()
        time.sleep_us(10)
        TRIG_PIN.low()
        
        # Wait for echo pulse start
        timeout_count = 0
        max_timeout = 10000
        
        while ECHO_PIN.value() == 0:
            timeout_count += 1
            if timeout_count > max_timeout:
                return -1  # Timeout
        pulse_start = time.ticks_us()
        
        # Wait for echo pulse end
        timeout_count = 0
        while ECHO_PIN.value() == 1:
            timeout_count += 1
            if timeout_count > max_timeout:
                return -1  # Timeout
        pulse_end = time.ticks_us()
        
        # Calculate distance
        pulse_duration = time.ticks_diff(pulse_end, pulse_start)
        distance_cm = (pulse_duration * 0.0343) / 2
        
        return distance_cm
        
    except:
        return -1


def get_distance():
    """
    Get validated distance measurement.
    Returns last valid reading if current reading is out of range.
    
    Returns:
        Distance in centimeters (integer)
    """
    global last_distance
    
    dist = get_distance_raw()
    
    # Validate distance (2cm to 400cm is valid range for HC-SR04)
    if 2 <= dist <= 400:
        last_distance = int(dist)
    
    return last_distance


# ==============================================================================
# OBSTACLE AVOIDANCE
# ==============================================================================

def avoid_obstacle():
    """
    Obstacle avoidance sequence.
    Stops the robot, backs up, performs a 180-degree turn, then resumes control.
    
    NOTE: Motors run at full speed - timing controls the distance/angle
    """
    global user_control_disabled, avoiding_obstacle, current_left_speed, current_right_speed
    global last_command_time, last_direction_change
    
    print("🚨 OBSTACLE! Backing up and turning 180°...")
    
    # Block all user commands during avoidance
    user_control_disabled = True
    avoiding_obstacle = True
    
    # Clear motor state
    current_left_speed = 0
    current_right_speed = 0
    
    # Step 1: STOP
    stop_all()
    time.sleep_ms(150)
    
    # Step 2: BACK UP (full speed backward)
    print("⬅️  Backing up...")
    set_motors_direct(-90, -90)  # Both motors backward (full speed)
    time.sleep_ms(AVOID_BACKUP_MS)  # Back up for configured duration
    stop_all()
    time.sleep_ms(100)
    
    # Step 3: 180-DEGREE TURN (randomly choose direction)
    turn_direction = random.choice(['LEFT', 'RIGHT'])
    print(f"🔄 Turning 180° {turn_direction}...")
    
    if turn_direction == 'LEFT':
        set_motors_direct(-90, 90)   # Tank turn left (full speed)
    else:
        set_motors_direct(90, -90)    # Tank turn right (full speed)
    
    time.sleep_ms(AVOID_TURN_MS)  # Turn for configured duration (~180°)
    
    # Step 4: STOP
    stop_all()
    
    # Step 5: CLEAR STATE
    current_left_speed = 0
    current_right_speed = 0
    
    # Reset timers
    last_command_time = time.ticks_ms()
    last_direction_change = time.ticks_ms()
    
    print("✅ Ready - Drive away!")
    
    # Delay to let user release joystick
    time.sleep_ms(300)
    
    # Re-enable user control
    user_control_disabled = False
    avoiding_obstacle = False


def check_obstacles():
    """
    Check for obstacles and trigger avoidance if needed.
    Only checks when moving forward and not already avoiding.
    """
    global last_sonar_check, current_left_speed, current_right_speed, in_tank_turn
    global last_direction_change
    
    # Rate limiting - don't check too frequently
    now = time.ticks_ms()
    if time.ticks_diff(now, last_sonar_check) < SONAR_CHECK_INTERVAL:
        return
    
    last_sonar_check = now
    
    # Don't check if already avoiding
    if avoiding_obstacle or user_control_disabled:
        return
    
    # Don't check during tank turns
    if in_tank_turn:
        return
    
    # Don't check immediately after direction change
    time_since_direction_change = time.ticks_diff(now, last_direction_change)
    if time_since_direction_change < DIRECTION_CHANGE_COOLDOWN:
        return
    
    # Only check if moving forward
    moving_forward = (current_left_speed > 15 or current_right_speed > 15)
    if not moving_forward:
        return
    
    # Get distance
    dist = get_distance()
    
    # Debug output
    if dist > 0:
        if dist < OBSTACLE_CRITICAL_CM:
            print(f"🚨 [SONAR] {dist}cm ⚠️⚠️ CRITICAL!")
        elif dist < OBSTACLE_DETECT_CM:
            print(f"⚠️  [SONAR] {dist}cm - WARNING!")
        else:
            print(f"📡 [SONAR] {dist}cm")
    
    # Trigger avoidance when obstacle detected while moving forward
    if 0 < dist < OBSTACLE_DETECT_CM:
        print(f">>> OBSTACLE DETECTED AT {dist}cm - AVOIDING!")
        avoid_obstacle()


# ==============================================================================
# COMMAND PARSER
# ==============================================================================

def parse_command(cmd):
    """
    Parse and execute commands from the Freenove app.
    
    NOTE: "speed" values from app are treated as direction indicators only
    
    Args:
        cmd: Command string from app
        
    Returns:
        True if command executed successfully
        String response for queries
        False if command invalid
    """
    global current_left_speed, current_right_speed, last_command_time
    global in_tank_turn, tank_turn_direction, user_control_disabled
    
    try:
        # Motor command: M#left#right#
        if cmd.startswith('M#'):
            # Ignore motor commands during obstacle avoidance
            if user_control_disabled or avoiding_obstacle:
                return True  # Discard command silently
            
            # Update timestamp
            last_command_time = time.ticks_ms()
            
            # Parse motor values (these indicate direction, not speed)
            parts = cmd[2:].strip('#').split('#')
            if len(parts) >= 2:
                left_raw = clamp(int(parts[0]))
                right_raw = clamp(int(parts[1]))
                
                # Apply deadzone
                left_speed = apply_deadzone(left_raw)
                right_speed = apply_deadzone(right_raw)
                
                final_left = 0
                final_right = 0
                
                # Check if both values are below minimum
                if abs(left_speed) < MIN_COMMAND_SPEED and abs(right_speed) < MIN_COMMAND_SPEED:
                    # Stop motors
                    final_left = 0
                    final_right = 0
                    if in_tank_turn:
                        in_tank_turn = False
                        tank_turn_direction = None
                else:
                    # Tank turn logic
                    if not in_tank_turn:
                        # Check if entering tank turn
                        if abs(left_speed) > TANK_ENTER_THRESHOLD and abs(right_speed) < TANK_ENTER_THRESHOLD:
                            in_tank_turn = True
                            tank_turn_direction = 'RIGHT'
                            last_direction_change = time.ticks_ms()
                        elif abs(right_speed) > TANK_ENTER_THRESHOLD and abs(left_speed) < TANK_ENTER_THRESHOLD:
                            in_tank_turn = True
                            tank_turn_direction = 'LEFT'
                            last_direction_change = time.ticks_ms()
                    else:
                        # Check if exiting tank turn
                        if tank_turn_direction == 'RIGHT':
                            if abs(right_speed) > TANK_EXIT_THRESHOLD:
                                in_tank_turn = False
                                tank_turn_direction = None
                                last_direction_change = time.ticks_ms()
                        elif tank_turn_direction == 'LEFT':
                            if abs(left_speed) > TANK_EXIT_THRESHOLD:
                                in_tank_turn = False
                                tank_turn_direction = None
                                last_direction_change = time.ticks_ms()
                    
                    # Apply tank turn or normal movement
                    if in_tank_turn:
                        if tank_turn_direction == 'RIGHT':
                            final_left = left_speed
                            final_right = -left_speed
                        elif tank_turn_direction == 'LEFT':
                            final_left = -right_speed
                            final_right = right_speed
                    else:
                        final_left = left_speed
                        final_right = right_speed
                
                # Update motor directions with thread safety
                with command_lock:
                    current_left_speed = final_left
                    current_right_speed = final_right
                    last_command_time = time.ticks_ms()
                
                return True
        
        # Control command: C#mode#
        elif cmd.startswith('C#'):
            parts = cmd.split('#')
            if len(parts) >= 2:
                mode = parts[1]
                if mode == '3':
                    # Distance query
                    dist = get_distance()
                    return f'SONIC:{dist}'
                else:
                    return 'OK'
        
        # Distance query (various formats)
        elif any(keyword in cmd.upper() for keyword in ['SONIC', 'DISTANCE', 'SONAR']):
            dist = get_distance()
            return f'SONIC:{dist}'
        
        # Status query
        elif 'STATUS' in cmd.upper():
            dist = get_distance()
            return f'STATUS:OK,DISTANCE:{dist}'
        
        return False
        
    except Exception as e:
        print(f"Parse error: {e}")
        return False


# ==============================================================================
# WIFI & SERVER
# ==============================================================================

def start_server():
    """
    Start WiFi connection and TCP server.
    Listens for commands from the Freenove app.
    """
    global last_command_time, last_sonar_check
    
    # ========================================================================
    # WIFI SETUP - EDIT THESE LINES WITH YOUR PHONE HOTSPOT INFO
    # ========================================================================
    # 1. Create a phone hotspot with a simple name (e.g., "Team1", "Robot2")
    # 2. Replace "YourHotspotName" with your hotspot name
    # 3. Replace "YourPassword" with your hotspot password
    # 4. Upload this code to your Pico
    # 5. Check Thonny console for the IP address when it connects
    # ========================================================================
    
    WIFI_SSID = "YourHotspotName"      # ← CHANGE THIS to your hotspot name
    WIFI_PASSWORD = "YourPassword"     # ← CHANGE THIS to your hotspot password
    
    # Connect to WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    print("Connecting to WiFi...")
    max_wait = 15
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('.', end='')
        LED.toggle()
        time.sleep(1)
    
    print()
    
    # Check connection status
    if wlan.status() != 3:
        print("WiFi connection FAILED!")
        LED.off()
        return
    
    # Get IP address
    ip = wlan.ifconfig()[0]
    
    # Print connection info
    print("=" * 50)
    print("✓ WiFi Connected!")
    print(f"IP Address: {ip}")
    print("=" * 50)
    print("4WD + AUTO OBSTACLE AVOIDANCE")
    print("=" * 50)
    print("Features:")
    print(f"  • Detects obstacles at {OBSTACLE_DETECT_CM}cm")
    print(f"  • Auto stops, backs up, and turns")
    print("  • Resumes user control after avoiding")
    print("=" * 50)
    print(f"Server: {ip}:5000")
    print("=" * 50)
    print("NOTE: Motors are DIRECTION-ONLY (full speed when ON)")
    print("=" * 50)
    LED.on()
    
    # Test ultrasonic sensor
    print("\n🔧 Testing ultrasonic sensor...")
    for i in range(5):
        dist = get_distance()
        print(f"  Test {i+1}: {dist}cm")
        time.sleep(0.3)
    
    print(f"\n✓ Sensor working! Last reading: {last_distance}cm")
    print()
    
    # Initialize
    stop_all()
    last_command_time = time.ticks_ms()
    last_sonar_check = time.ticks_ms()
    
    # Create TCP server
    addr = socket.getaddrinfo('0.0.0.0', 5000)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    
    print("Server listening...")
    print("🚗 AUTO-AVOID ACTIVE - Drive safely!")
    print()
    
    # Main server loop
    while True:
        try:
            # Accept client connection
            cl, addr = s.accept()
            print(f"🎮 APP CONNECTED: {addr}\n")
            cl.settimeout(0.05)
            
            # Client communication loop
            while True:
                try:
                    # Receive data
                    data = cl.recv(1024)
                    if not data:
                        break
                    
                    # Parse commands
                    raw_data = data.decode('utf-8').strip()
                    commands = raw_data.split('\n')
                    
                    for cmd in commands:
                        cmd = cmd.strip()
                        if cmd:
                            result = parse_command(cmd)
                            
                            # Send response
                            if result is True:
                                cl.send(b'OK\n')
                            elif isinstance(result, str):
                                cl.send(result.encode() + b'\n')
                            else:
                                cl.send(b'ERROR\n')
                    
                    # Check for obstacles
                    check_obstacles()
                
                except OSError:
                    # Timeout - check obstacles anyway
                    check_obstacles()
                except Exception as e:
                    print(f"Communication error: {e}")
                    break
            
            # Client disconnected
            cl.close()
            stop_all()
            print("\n🎮 App disconnected\n")
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            stop_all()
            LED.off()
            break
        except Exception as e:
            print(f"Connection error: {e}")
            try:
                cl.close()
            except:
                pass


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""
    print("=" * 50)
    print("4WD Robot - Auto Obstacle Avoidance")
    print("Direction Control Only (Full Speed)")
    print("=" * 50)
    
    try:
        start_server()
    except Exception as e:
        print(f"Fatal error: {e}")
        stop_all()
        LED.off()


if __name__ == '__main__':
    main()
