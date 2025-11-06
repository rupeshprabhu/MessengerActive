import subprocess
import time
import sys
import psutil

APP_ENTRY = "main.py"

def test_single_instance_blocking():
    """Ensure a second instance cannot run concurrently."""
    # Launch first instance
    first = subprocess.Popen([sys.executable, APP_ENTRY])
    time.sleep(2)  # give time for mutex creation

    # Launch second instance
    second = subprocess.Popen([sys.executable, APP_ENTRY], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

    # Get all running python processes
    procs = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name'].lower()]

    # There should be only one active instance of main.py
    count = 0
    for p in procs:
        try:
            cmdline = psutil.Process(p['pid']).cmdline()
            if APP_ENTRY in " ".join(cmdline):
                count += 1
        except Exception:
            pass

    # Terminate both
    first.terminate()
    second.terminate()

    assert count <= 1, f"Expected single instance, found {count}"
