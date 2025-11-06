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

# --- Import main safely ---
try:
    from main import simulate_keypress, keep_screen_awake, running
except ModuleNotFoundError:
    pytest.skip("main.py not found or import failed — skipping tests.", allow_module_level=True)


def test_simulate_keypress():
    """Ensure simulate_keypress function executes without throwing."""
    try:
        simulate_keypress()
    except Exception as e:
        pytest.fail(f"simulate_keypress() raised an exception: {e}")


def test_thread_running_flag():
    """Ensure running flag is properly defined and boolean."""
    assert isinstance(running, bool)


@pytest.mark.timeout(10)
def test_single_instance_behavior():
    """
    Ensure only one instance of the app can run at once.
    The second instance should detect the first and exit.
    """
    main_path = os.path.join(ROOT_DIR, "main.py")
    assert os.path.exists(main_path), "main.py not found"

    # Start first process
    process1 = subprocess.Popen(
        [sys.executable, main_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)

    # Start second process
    process2 = subprocess.Popen(
        [sys.executable, main_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)

    # Collect process info
    processes = [
        p.info for p in psutil.process_iter(["pid", "name", "cmdline"])
        if p.info["cmdline"] and "main.py" in " ".join(p.info["cmdline"])
    ]

    # There should be at most one MessengerActive instance
    assert len(processes) <= 1, f"Multiple instances found: {len(processes)}"

    # Cleanup
    for p in [process1, process2]:
        try:
            p.terminate()
        except Exception:
            pass
