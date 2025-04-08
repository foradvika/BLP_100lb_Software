# BLP 100lb Test Control Software

This software controls and monitors the BLP 100lb test system, providing a graphical interface for valve control, test sequence execution, and system monitoring.

## Features

- Valve control interface
- Test sequence execution
- Real-time system monitoring
- Data logging and visualization
- Emergency abort functionality

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python src/main.py
```

## Project Structure

```
src/
├── control/
│   ├── telemetry.py      # Telemetry control system
│   └── test_sequence.py  # Test sequence management
├── gui/
│   └── main_window.py    # Main GUI window
└── main.py               # Application entry point
```

## License

MIT License
