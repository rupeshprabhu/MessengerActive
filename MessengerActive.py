import ctypes
import time
import threading
import logging
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw
import pystray
import win32api
import win32con
from winotify import Notification
import win32event
import winerror
import win32gui

APP_NAME = "MessengerActive"

# === Single Instance Protection ===
MUTEX_NAME = f"{APP_NAME}_SINGLE_INSTANCE"

mutex = win32event.CreateMutex(None, False, MUTEX_NAME)
last_error = win32api.GetLastError()

def bring_existing_window_to_front():
    """Locate and focus the existing MessengerActive window if it exists."""
    try:
        hwnd = win32gui.FindWindow(None, APP_NAME)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
    except Exception:
        pass
    return False

if last_error == winerror.ERROR_ALREADY_EXISTS:
    # Another instance already running
    if not bring_existing_window_to_front():
        ctypes.windll.user32.MessageBoxW(
            0,
            f"{APP_NAME} is already running.",
            APP_NAME,
            0x40  # MB_ICONINFORMATION
        )
    sys.exit(0)

# === Version Read ===
with open(os.path.join(os.path.dirname(__file__), "version.txt"), "r") as vf:
    APP_VERSION = vf.read().strip()

# === Logging setup ===
appdata_path = os.getenv("APPDATA")
log_dir = os.path.join(appdata_path, APP_NAME)
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "activity.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

running = True
tray_icon = None
has_shown_tray_message = False

# === Resolve base path for icon (PyInstaller compatibility) ===
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, "ma_icon.ico")

ICON_IMG = None
try:
    if os.path.exists(icon_path):
        ICON_IMG = Image.open(icon_path)
    else:
        # fallback: create a tiny placeholder icon (32x32 RGBA)
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((4, 4, 28, 28), fill=(0, 120, 215, 255))
        ICON_IMG = img
except Exception as e:
    logging.error(f"Failed to load/create icon image: {e}")
    ICON_IMG = None

# === Set AppUserModelID for taskbar icon and notifications (Windows) ===
if os.name == "nt":
    try:
        app_id = f"{APP_NAME}.{APP_VERSION}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        logging.error(f"AppUserModelID failed: {e}")

# Execution state constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def simulate_keypress():
    """A tiny keypress to keep some systems from considering the user idle."""
    try:
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        logging.debug("Simulated keypress.")
    except Exception as e:
        logging.error(f"simulate_keypress failed: {e}")

def keep_screen_awake():
    """Thread target to periodically prevent sleep and inject occasional keypresses."""
    last_keypress = time.time()
    while running:
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
        except Exception as e:
            logging.error(f"SetThreadExecutionState failed: {e}")

        if time.time() - last_keypress >= 300:  # every 5 minutes
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
            duration="short" if duration < 10 else "long",
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
        pystray.MenuItem("Exit", on_exit_from_tray),
    )

    tray_icon = pystray.Icon(APP_NAME, ICON_IMG, f"{APP_NAME} Running", menu)
    try:
        tray_icon.run_detached()
    except Exception as e:
        logging.error(f"Failed to run tray icon: {e}")

def hide_tray_icon():
    global tray_icon
    if tray_icon:
        try:
            tray_icon.stop()
        except Exception as e:
            logging.error(f"Failed to stop tray icon: {e}")
        tray_icon = None

def on_minimize(event=None):
    global has_shown_tray_message
    try:
        root.withdraw()
        show_tray_icon()
        if not has_shown_tray_message:
            has_shown_tray_message = True
            show_notification(APP_NAME, "MessengerActive minimized to system tray.")
            logging.info("App minimized to tray.")
    except Exception as e:
        logging.error(f"on_minimize failed: {e}")

def on_exit_confirm():
    confirm = tk.Toplevel(root)
    confirm.title("Exit MessengerActive")
    confirm.geometry("360x160")
    confirm.resizable(False, False)
    confirm.attributes("-topmost", True)

    ttk.Label(
        confirm,
        text="Do you really want to exit MessengerActive?\n\n"
             "Tip: You can minimize it to system tray to keep it running\n"
             "in the background with minimal resource use.",
        wraplength=320,
        justify="center",
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
    try:
        root.destroy()
    except Exception:
        pass

# === Tkinter Setup ===
root = tk.Tk()
root.title(APP_NAME)
root.geometry("300x110")
root.resizable(False, False)

try:
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except Exception as e:
    logging.error(f"Icon set failed: {e}")

# Center window on screen
x = (root.winfo_screenwidth() - 300) // 2
y = (root.winfo_screenheight() - 110) // 2
root.geometry(f"300x110+{x}+{y}")

# UI Elements
ttk.Label(root, text="Teams is Active", font=("Segoe UI", 11)).pack(pady=10)
ttk.Button(root, text="Exit", command=on_exit_confirm).pack()

# Bind minimize and close events
root.protocol("WM_DELETE_WINDOW", on_exit_confirm)
root.bind("<Unmap>", lambda e: on_minimize() if root.state() == "iconic" else None)

# Start the keep-awake thread
threading.Thread(target=keep_screen_awake, daemon=True).start()

if __name__ == "__main__":
    logging.info("MessengerActive started.")
    root.mainloop()
    logging.info("MessengerActive stopped.")
