# BLP Hardware-Software Communication Protocol

## 1. Serial Communication
- Port: COM7 (Windows) or /dev/ttyACM0 (Linux)
- Baud Rate: 115200
- Data Bits: 8
- Stop Bits: 1
- Parity: None

## 2. Data Packet Format

### Command Packet (Software → Hardware)
```
[heartbeat][valve1][valve2][valve3][valve4][coil][coil_speed][abort]
```
- Each field is 1 byte
- Values:
  - heartbeat: -49 (0xCF)
  - valves: 0 (closed) or 1 (open)
  - coil: 0 (off) or 1 (on)
  - coil_speed: 0-255 (PWM value)
  - abort: 0 (normal) or 1 (abort)

### Response Packet (Hardware → Software)
```
[status][valve1_fb][valve2_fb][valve3_fb][valve4_fb][pt1][pt2][pt3][pt4][pt5][thrust]
```
- Each field is 2 bytes (16-bit integer)
- Values:
  - status: System status code
  - valve_fb: 0 (closed) or 1 (open)
  - pt1-pt5: Pressure transducer readings (PSI)
  - thrust: Thrust reading (lbf)

## 3. Timing Requirements
- Command response time: < 100ms
- Sensor update rate: 10Hz
- Valve actuation time: < 500ms

## 4. Error Handling
- Hardware timeout: 1 second
- Retry attempts: 3
- Error codes:
  - 0x00: Success
  - 0x01: Communication error
  - 0x02: Valve error
  - 0x03: Sensor error
  - 0x04: System error

## 5. Safety Protocols
1. All valves must be closed at startup
2. Abort command must close all valves
3. Pressure limits:
   - PT1 (OPD_02): < 350 PSI
   - PT2 (FPD_02): < 530 PSI
   - PT3 (EPD_01): < 825 PSI
4. Minimum pressure checks:
   - All pressure transducers: > 15 PSI

## 6. Test Sequence Requirements
1. Must include abort command
2. Valve operations must be sequential
3. Pressure checks must precede valve operations
4. Maximum test duration: 60 seconds 