import ctypes
import time
import threading
import logging
import win32api
import win32con
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from PIL import Image
import pystray

# === Prevent system sleep constants ===
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002

# === App info ===
APP_NAME = "MessengerActive"
APP_VERSION = "1.0"

# === Setup logging directory in %APPDATA% ===
appdata_path = os.getenv('APPDATA')
log_dir = os.path.join(appdata_path, APP_NAME)
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'activity.log')

# === Configure logging ===
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# === Global control flag ===
running = True
tray_icon = None
root = None

# === Keep screen awake logic ===
def simulate_keypress():
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
    logging.info("Simulated Shift key press to prevent idle state.")

def keep_screen_awake():
    logging.info("Screen activity thread started.")
    last_keypress_time = time.time()
    while running:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)
        logging.info("SetThreadExecutionState called to keep screen active.")
        if time.time() - last_keypress_time >= 300:
            simulate_keypress()
            last_keypress_time = time.time()
        time.sleep(30)

# === Graceful exit ===
def on_exit():
    global running, tray_icon
    running = False
    if tray_icon:
        tray_icon.stop()
    root.destroy()

# === Handle minimize to tray ===
def on_minimize(event=None):
    root.withdraw()
    show_tray_icon()

def on_show_window(icon=None, item=None):
    root.deiconify()
    root.after(0, root.focus_force)
    hide_tray_icon()

def on_exit_from_tray(icon=None, item=None):
    on_exit()

# === Tray icon functions ===
def show_tray_icon():
    global tray_icon
    if tray_icon is not None:
        return

    # Load tray icon image
    image = None
    if os.path.exists(icon_path):
        image = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("Show", on_show_window),
        pystray.MenuItem("Exit", on_exit_from_tray)
    )

    tray_icon = pystray.Icon(APP_NAME, image, f"{APP_NAME} Running", menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()

def hide_tray_icon():
    global tray_icon
    if tray_icon:
        tray_icon.stop()
        tray_icon = None

# === Resolve icon path correctly (handles both Python and PyInstaller modes) ===
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller unpacked temp folder
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'ma_icon.ico')

# === Start background thread ===
threading.Thread(target=keep_screen_awake, daemon=True).start()

# === GUI setup ===
root = tk.Tk()
root.title(APP_NAME)
root.geometry("250x100")
root.resizable(False, False)

# === Set AppUserModelID and icon (fixes taskbar + title bar icon) ===
if os.name == 'nt':
    try:
        # Must be called before window creation for consistent taskbar icon
        app_id = f"{APP_NAME}.{APP_VERSION}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        logging.error(f"Failed to set AppUserModelID: {e}")

# === Set the window icon ===
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    try:
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        icon_handle = ctypes.windll.user32.LoadImageW(
            None, icon_path, 1, 0, 0, 0x00000010  # IMAGE_ICON = 1, LR_LOADFROMFILE = 0x10
        )
        # Apply icon for both large and small versions (title + taskbar)
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, icon_handle)  # WM_SETICON (large)
        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, icon_handle)  # WM_SETICON (small)
    except Exception as e:
        logging.error(f"Failed to set window icon: {e}")
else:
    logging.warning(f"Icon file not found: {icon_path}")

# === Center window ===
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (250 / 2))
y = int((screen_height / 2) - (100 / 2))
root.geometry(f"250x100+{x}+{y}")

# === UI elements ===
style = ttk.Style()
style.theme_use('clam')

label = ttk.Label(root, text="Teams is Active", font=("Segoe UI", 11))
label.pack(pady=10)

exit_button = ttk.Button(root, text="Exit", command=on_exit)
exit_button.pack()

# === Bind minimize event to tray ===
root.protocol("WM_DELETE_WINDOW", on_minimize)
root.bind("<Unmap>", lambda e: on_minimize() if root.state() == 'iconic' else None)

# === Main loop ===

root.mainloop()
