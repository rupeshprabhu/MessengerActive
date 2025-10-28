import threading
import time
import ctypes
import win32api
import win32con

from main import keep_screen_awake, simulate_keypress, running

def test_simulate_keypress():
    """Ensure simulate_keypress runs without error."""
    try:
        simulate_keypress()
    except Exception as e:
        assert False, f"simulate_keypress failed: {e}"

def test_thread_alive():
    """Ensure keep_screen_awake thread runs and sets execution state."""
    thread = threading.Thread(target=keep_screen_awake, daemon=True)
    thread.start()
    time.sleep(2)
    assert thread.is_alive(), "Thread not alive"

def test_imports():
    """Check all major imports load correctly."""
    try:
        import tkinter
        import pystray
        import winotify
    except ImportError as e:
        assert False, f"Import failed: {e}"
