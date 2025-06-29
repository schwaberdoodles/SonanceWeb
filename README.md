# SonanceWeb

**SonanceWeb** is an open-source, web-based controller for the classic  
[Sonance DAB1 distributed audio system](http://www.soundandvision.com/content/sonance-dab1-distributed-audio-system).  
Control your home’s audio zones with an intuitive HTML5 interface — right from any browser.

---

## 🚀 Project Highlights

- Modern Python 3 codebase (originally Python 2.7)
- Tested on Raspberry Pi + RS232 serial null modem cable to DAB1
- Communicates with Sonance DAB1 via its serial protocol
- Easily configure host/port via environment variables  
  (`SONANCE_SERVER_HOSTNAME` and `SONANCE_SERVER_PORT`)
- **Not maintained** — code is provided as-is!

---

## 🖥️ How It Works

SonanceWeb relies on [pyserial’s `tcp_serial_redirect`](https://pyserial.readthedocs.io/en/latest/tools.html#tcp-serial-redirect):  
- A TCP server (usually on `localhost:7777`) proxies all serial commands to your DAB1 device.
- SonanceWeb connects via TCP and exposes a simple web UI to control all DAB1 zones.

---

## 🛠️ Requirements

- Python 3.x
- pyserial 2.7 (`pip install pyserial`)

---

## ⚠️ Notes & Caveats

- You **must** have `tcp_serial_redirect` running and attached to the DAB1's serial port.
- This project is **no longer maintained**. PRs and issues may not be reviewed.
- Use at your own risk!

---

## 📦 Quickstart

```sh
# Install dependencies
pip install pyserial flask

# Run the serial redirect (adjust tty/COM port as needed)
python -m serial.tools.tcp_serial_redirect -P 7777 -p /dev/ttyUSB0

# Set environment variables as needed
export SONANCE_SERVER_HOSTNAME=localhost
export SONANCE_SERVER_PORT=7777

# Start the web server
python sonanceweb.py
