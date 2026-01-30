# TY Robotics Program 2026 🤖

Welcome to the **Transition Year Robotics Program** at IBM Waterford!

This repository contains all the materials you'll need for the week-long robotics program (February 2-6, 2026).

## 📅 Program Schedule

- **Monday:** Program overview (with IBM & partner organizations)
- **Tuesday:** Python basics + Robot assembly
- **Wednesday:** Advanced Python + Robot programming
- **Thursday:** Competition preparation (debugging, customization, practice)
- **Friday:** IBM AI session + **ROBOT COMPETITION!** 🏆

## 🚀 Getting Started

### 1. Download This Repository

Click the green **"Code"** button at the top of this page, then click **"Download ZIP"**. Extract the files to your computer.

### 2. Install Thonny

Download and install **Thonny Python IDE** from [thonny.org](https://thonny.org)

### 3. Connect Your Robot

1. Connect your Raspberry Pi Pico to your computer via USB
2. Open Thonny
3. Select **"MicroPython (Raspberry Pi Pico)"** from the interpreter menu

### 4. Start Coding!

Open the challenge or program you want to work on from the folders above.

## 🐛 Thursday Debug Challenges

These files contain bugs that you need to find and fix:

| Challenge | Difficulty | Bugs | Description |
|-----------|------------|------|-------------|
| **Challenge 1** | EASY | 2 bugs | Motor test - all wheels should spin forward |
| **Challenge 2** | MEDIUM | 3 bugs | Sensor reading - should display distance |
| **Challenge 3** | HARD | 2 bugs | Square pattern - robot should drive in a square |

## 🤖 Thursday Behavior Programs

Complete these programs with progressive difficulty:

| Program | Difficulty | Description |
|---------|------------|-------------|
| **Behavior 1** | EASY (Guided) | Drive in a perfect square |
| **Behavior 2** | EASY | Spin 360° in place |
| **Behavior 3** | MEDIUM | Move forward until obstacle detected |
| **Behavior 4** | MEDIUM | Drive in figure-8 pattern |
| **Behavior 5** | HARD | Continuous obstacle avoidance |

## 📱 Robot Control

### Your Robot: 4WD Car Kit for Raspberry Pi Pico(w)

**Components:**
- Raspberry Pi Pico W
- 4 wheels (2 front, 2 rear)
- 2 motor drivers
- 1 ultrasonic distance sensor
- WiFi capability

### WiFi Setup

1. Create a phone hotspot with a simple name (e.g., "Team1")
2. Edit `main.py` and change the WiFi credentials:
   ```python
   WIFI_SSID = "YourHotspotName"
   WIFI_PASSWORD = "YourPassword"
   ```
3. Upload to your Pico
4. Note the IP address shown in Thonny console
5. Open Freenove app and connect to that IP address (port 5000)

### Freenove App

**Download:**
- **iPhone/iPad:** App Store → Search "Freenove"
- **Android:** Google Play Store → Search "Freenove"

**Note:** Only ONE person per team needs the app!

## 🔧 Main Robot Code (main.py)

The complete robot control program includes:
- ✅ WiFi control via Freenove app
- ✅ Automatic obstacle avoidance
- ✅ Tank turn steering
- ✅ Ultrasonic distance sensing
- ✅ Direction-only motor control (full speed)

### Customizable Settings (in main.py):

```python
OBSTACLE_DETECT_CM = 20    # Detection distance (try 15-40)
AVOID_BACKUP_MS = 600      # Backup time (try 400-1000)
AVOID_TURN_MS = 1200       # Turn time - 1200ms ≈ 180°
```

## 💡 Tips for Success

### Debugging
- Read error messages carefully - they tell you what's wrong
- Check for typos in variable names
- Make sure indentation is correct (Python is strict about this!)
- Test frequently - don't write too much code before testing

### Programming
- Start with EASY challenges to build confidence
- Work with your partner - collaborate!
- Ask instructors when stuck
- Comment your code so you remember what it does

### Testing
- Always test on the actual robot
- Start in a clear, open area
- Have someone ready to catch the robot if needed
- Adjust timing values if movements aren't quite right

## 🏆 Friday Competition

Use Thursday afternoon to:
1. ✅ Customize your obstacle avoidance settings
2. ✅ Choose your strategy (aggressive/conservative/balanced)
3. ✅ Practice on the actual competition course
4. ✅ Fine-tune timing and detection distances
5. ✅ Test, test, test!

**Goal:** Navigate the obstacle course autonomously - furthest distance wins!

## 📚 Additional Resources

- **Thonny Documentation:** [docs.thonny.org](https://docs.thonny.org)
- **MicroPython Docs:** [docs.micropython.org](https://docs.micropython.org)
- **Raspberry Pi Pico:** [raspberrypi.com/documentation/microcontrollers](https://www.raspberrypi.com/documentation/microcontrollers/)

## 🤝 Getting Help

**During the Program:**
- Ask your instructors (IBM, Red Hat, SETU staff)
- Work with your team members
- Check the README files in each folder

**Have Questions?**
- Check the presentation slides in the `Presentations/` folder
- Review the reference materials
- Don't be afraid to experiment!

## ⚠️ Important Notes

- **Save your work frequently!**
- **Don't modify the original BROKEN/STARTER files** - make copies if needed
- **Test in a safe area** - robots can move fast!
- **Battery care** - unplug when not in use
- **Have fun!** This is about learning and creating 🎉

## 🎓 Learning Outcomes

By the end of this program, you'll be able to:
- ✅ Write Python code for hardware control
- ✅ Debug code and fix common errors
- ✅ Use sensors to make decisions
- ✅ Program autonomous robot behavior
- ✅ Collaborate on technical projects
- ✅ Problem-solve under pressure

---

## 🚀 Let's Build Something Amazing!

Good luck with your robots! Remember - every bug you fix makes you a better programmer, and every challenge you complete builds your skills.

**See you at the competition on Friday!** 🏁

---

**Program Partners:**
- 🔵 **IBM Waterford**
- 🔴 **Red Hat**
- 🎓 **SETU (South East Technological University)**

*Last Updated: January 30, 2026*
