# 📨 MessengerActive  
> Keep your PC awake and Microsoft Teams active — automatically ⚡  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-PyInstaller-orange?logo=appveyor)

---

## 🌟 Overview

**MessengerActive** is a lightweight Windows utility built in Python 🐍 that keeps your system awake and **prevents Teams or other chat apps from showing you as “Away.”**

It simulates small background activity, ensuring your PC stays active — without interfering with your work.

### ✨ Features
- 💤 Prevents screen sleep and idle mode  
- 💬 Keeps Teams or Slack status “Active”  
- ⚙️ Runs silently in the background  
- 🪟 Modern Tkinter GUI  
- 🪶 Custom app & taskbar icon  
- 🧩 Optional System Tray (minimize-to-tray support)  
- 🧠 Lightweight — uses minimal CPU and memory  

---

## 🖥️ Screenshot




##⚙️ Installation
#🧱 Requirements
-Windows 10 or 11
-Python 3.9+

pip install -r requirements.txt

## 🪶 Install Dependencies
pip install pystray pillow pywin32

## ▶️ Run from Source
python messenger_active.py

## 🏗️ Build as EXE with PyInstaller

You can package the app into a single .exe (no console) using:

pyinstaller --clean MessengerActive.spec

pyinstaller --noconsole --icon=raphael_icon.ico --add-data "ma_icon.ico;." MessengerActive.py


Your compiled file will appear in:

/dist/messenger_active.exe

## 🪟 System Tray Mode

When you minimize or close the window:

The app continues running in the background.

A tray icon appears in your taskbar.

Right-click it for options:

🟢 Show – Restore the window

🔴 Exit – Quit gracefully

## 🧠 How It Works

Calls SetThreadExecutionState to prevent display sleep 🖥️

Simulates harmless keypresses (Shift) periodically ⌨️

Keeps your user session “active” for chat and presence apps 💬

## 🧾 Logging

MessengerActive logs its activity to:

%APPDATA%\MessengerActive\activity.log


Each simulated keypress and system action is timestamped for visibility.

## 📦 Folder Structure
MessengerActive/
│
├── messenger_active.py     # Main app
├── raphael_icon.ico        # Application icon
├── requirements.txt        # Python dependencies
├── README.md               # This file ✨
└── dist/                   # PyInstaller output (after build)

## ⚠️ Notes

The app does not interfere with keyboard input.

It uses only system-level APIs (win32api, SetThreadExecutionState).

Fully local — no network or telemetry.

## 🛠️ Troubleshooting
Issue	Solution
-❌ Icon not showing in taskbar	Ensure you built with --icon=raphael_icon.ico
-⚙️ Error: pystray not found	Run pip install pystray pillow pywin32
-💤 PC still sleeps	Check if company policy overrides sleep prevention
##📜 License

Released under the MIT License.
You’re free to use, modify, and distribute this project — just keep the license file attached.

## 💡 Author

Created with ❤️ by Rupesh Prabhu
If you like this project, give it a ⭐ on GitHub — it helps others discover it!

## 🚀 Future Ideas
-⏰ Custom idle interval configuration
-🪟 Dark mode UI
-📢 Toast notifications when minimizing to tray
