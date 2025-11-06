import sys
import os
import subprocess
import time
import psutil
import pytest

# --- Ensure root path is added ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Now import your main functions
from main import simulate_keypress, keep_screen_awake, running


def test_simulate_keypress():
    """Ensure simulate_keypress function executes without throwing."""
    try:
        simulate_keypress()
    except Exception as e:
        pytest.fail(f"simulate_keypress() raised an exception: {e}")


def test_thread_running_flag():
    """Ensure running flag is properly defined and boolean."""
    assert isinstance(running, bool)


def test_single_instance_behavior():
    """Ensure only one instance of app can run at once."""
    process1 = subprocess.Popen(
        [sys.executable, "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)

    process2 = subprocess.Popen(
        [sys.executable, "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)

    # Count running processes with 'main.py' in command
    processes = [
        p.info for p in psutil.process_iter(["pid", "name", "cmdline"])
        if p.info["cmdline"] and "main.py" in " ".join(p.info["cmdline"])
    ]
    assert len(processes) <= 1, f"Multiple instances found: {len(processes)}"

    for p in [process1, process2]:
        p.terminate()
