import ctypes
import time
import threading
import logging
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image
import pystray
import win32api
import win32con
from winotify import Notification

APP_NAME = "MessengerActive"
APP_VERSION = "1.0"

# === Logging setup ===
appdata_path = os.getenv('APPDATA')
log_dir = os.path.join(appdata_path, APP_NAME)
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'activity.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

running = True
tray_icon = None
has_shown_tray_message = False

# === Resolve base path for icon (PyInstaller compatibility) ===
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, "ma_icon.ico")

ICON_IMG = None
try:
    if os.path.exists(icon_path):
        ICON_IMG = Image.open(icon_path)
except Exception as e:
    logging.error(f"Failed to load icon image: {e}")

# === Set AppUserModelID for taskbar icon and notifications (Windows) ===
if os.name == 'nt':
    try:
        app_id = f"{APP_NAME}.{APP_VERSION}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        logging.error(f"AppUserModelID failed: {e}")

def simulate_keypress():
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)

def keep_screen_awake():
    last_keypress = time.time()
    while running:
        # Prevent system sleep and display off
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000002)
        if time.time() - last_keypress >= 300:
            simulate_keypress()
            last_keypress = time.time()
        time.sleep(30)

def show_notification(title, msg, duration=5):
    try:
        toast = Notification(
            app_id=APP_NAME,
            title=title,
            msg=msg,
            icon=icon_path if os.path.exists(icon_path) else None,
            duration="short" if duration < 10 else "long"
        )
        toast.show()
    except Exception as e:
        logging.error(f"Notification failed: {e}")

def on_show_window(icon, item):
    root.after(0, lambda: [root.deiconify(), hide_tray_icon()])

def on_exit_from_tray(icon, item):
    root.after(0, on_exit_confirm)

def show_tray_icon():
    global tray_icon
    if tray_icon:
        return

    menu = pystray.Menu(
        pystray.MenuItem("Show", on_show_window),
        pystray.MenuItem("Exit", on_exit_from_tray)
    )

    tray_icon = pystray.Icon(APP_NAME, ICON_IMG, f"{APP_NAME} Running", menu)
    tray_icon.run_detached()

def hide_tray_icon():
    global tray_icon
    if tray_icon:
        tray_icon.stop()
        tray_icon = None

def on_minimize(event=None):
    global has_shown_tray_message
    root.withdraw()
    show_tray_icon()
    if not has_shown_tray_message:
        has_shown_tray_message = True
        show_notification(APP_NAME, "MessengerActive minimized to system tray.")
        logging.info("App minimized to tray.")

def on_exit_confirm():
    confirm = tk.Toplevel(root)
    confirm.title("Exit MessengerActive")
    confirm.geometry("320x150")
    confirm.resizable(False, False)
    confirm.attributes('-topmost', True)

    ttk.Label(
        confirm,
        text="Do you really want to exit MessengerActive?\n\n"
             "Tip: You can minimize it to system tray to keep it running\n"
             "in the background with minimal resource use.",
        wraplength=300, justify="center"
    ).pack(pady=15)

    button_frame = ttk.Frame(confirm)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Minimize Instead", command=lambda: [confirm.destroy(), on_minimize()]).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Exit", command=lambda: [confirm.destroy(), on_exit()]).grid(row=0, column=1, padx=10)

def on_exit():
    global running
    running = False
    hide_tray_icon()
    show_notification(APP_NAME, "MessengerActive has been closed.")
    root.destroy()

# === Tkinter Setup ===
root = tk.Tk()
root.title(APP_NAME)
root.geometry("250x100")
root.resizable(False, False)

try:
    root.iconbitmap(icon_path)
except Exception as e:
    logging.error(f"Icon set failed: {e}")

# Center window on screen
x = (root.winfo_screenwidth() - 250) // 2
y = (root.winfo_screenheight() - 100) // 2
root.geometry(f"250x100+{x}+{y}")

# UI Elements
ttk.Label(root, text="Teams is Active", font=("Segoe UI", 11)).pack(pady=10)
ttk.Button(root, text="Exit", command=on_exit_confirm).pack()

# Bind minimize and close events
root.protocol("WM_DELETE_WINDOW", on_exit_confirm)
root.bind("<Unmap>", lambda e: on_minimize() if root.state() == 'iconic' else None)

# Start the keep-awake thread
threading.Thread(target=keep_screen_awake, daemon=True).start()

root.mainloop()
