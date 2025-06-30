# Project: Controllable Self-Balancing Robot with Follow Mode

## 🗂️ Project Management Guidelines
- Break down work into **small, concrete tasks** (1 day or less)
- Include a mix of: **documentation, research, wiring, testing, coding, configuration**
- Acknowledge technical blockers and investigation tasks
- Avoid vague or high-level issues; tasks should be **actionable and clear**
- Each issue must ideally have a measurable outcome

---

## 🎯 Goals
- Maintain upright balance using a Pixhawk 2 flight controller
- Accept RC input for manual control via radio receiver
- Enable GPS-based autonomous missions
- Implement "follow" mode (e.g., following a Bluetooth/IR/GPS beacon)
- Build the system in a modular, testable, and maintainable way

---

## 🔧 Hardware Components
- **Pixhawk 2 Cube** — flight controller with GPS, RC, and telemetry support
- **RioRand motor controller** — controls 3-phase BLDC motors using DIR/SPEED/BRAKE/HALL inputs
- **Two hoverboard motors** — brushless DC motors with hall feedback
- **Arduino Uno or Nano** — interfaces between Pixhawk and motor controller
- **RC transmitter/receiver**
- **Beacon sensor** — e.g., Bluetooth RSSI, GPS phone, or IR beacon
- **Power system** — battery pack, voltage regulator, distribution wiring

---

## 📆 Milestones and Technical Breakdown

### 1. Project Documentation & Planning
- Write README.md with goals, system overview, and responsibilities
- Research free tools for drawing architecture and control flow diagrams (e.g., draw.io, diagrams.net, Mermaid)
- Create system architecture diagram: sensors, logic units, motors, power
- Draft control flow between Pixhawk → Arduino → Motor Controller
- Document known challenges and unknowns (e.g., Pixhawk to Arduino comms, hall feedback handling)

---

### 2. Parts List & Procurement
- Compile a complete BOM (Bill of Materials) with links, quantities, and prices
- Estimate current draw per component (e.g., motors, Arduino, Pixhawk)
- Research wiring needs (connectors, heat shrink, fuse/relay, PCBs?)
- Add items to part-tracking spreadsheet (CSV or Git-tracked file)
- Order/procure initial hardware for testing

---

### 3. Mechanical Build & Wiring Layout
- Design and build chassis/platform to mount all components
- Wire motor controller to hoverboard motors and test secure connections
- Connect and verify hall sensor feedback wiring
- Design wiring layout between Arduino and motor controller
- Plan and document power design: battery specs, voltage regulation, power switches
- Document wiring in schematic/diagram format

---

### 4. Arduino: Motor Control Firmware
- Write a minimal Arduino sketch to control one motor (DIR, SPEED, BRAKE)
- Use hall sensor feedback to calculate RPM and log to serial
- Refactor sketch to independently control two motors
- Add serial debug logging for DIR/BRAKE/RPM
- Document command interface between Arduino and motor controller (timing, voltage, logic)

---

### 5. Pixhawk to Arduino Integration
- Research communication options (PWM vs MAVLink serial vs SBUS)
- Configure Pixhawk to output usable PWM signal to Arduino
- Read Pixhawk PWM on Arduino and map to speed/direction control
- Test motor response to RC override from Pixhawk
- Measure response delay between Pixhawk input → Arduino output

---

### 6. RC Input Configuration
- Connect RC receiver to Pixhawk (PPM/SBUS input)
- Calibrate RC channels in QGroundControl or Mission Planner
- Verify channel mapping (pitch/roll/throttle) in RC test mode
- Check signal passthrough from RC → Pixhawk → Arduino → Motors

---

### 7. GPS Integration & Testing
- Mount GPS antenna on chassis and connect to Pixhawk
- Acquire GPS lock and log telemetry in Mission Planner
- Simulate a simple autonomous mission with GPS waypoints
- Ensure Arduino doesn’t interfere with Pixhawk's mission execution

---

### 8. Follow Mode Development (Sensor-Based)
- Evaluate options: Bluetooth RSSI, GPS beacon, or IR tracking
- Test chosen sensor’s data quality in indoor conditions
- Write Arduino code to interpret beacon sensor signal (distance or direction)
- Translate signal into motor speed/direction adjustments
- Perform controlled indoor “follow me” tests with dummy beacon

---

## 📌 Notes
- Use GitLab issues to track progress in small testable units
- Keep a changelog in the repository for hardware & software updates
- Start simple and iterate: one motor, one sensor, one command at a time

