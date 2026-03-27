from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import threading

BASE_DIR = r"D:\System Stuff\Gained Certificates"
CERT_DIR = BASE_DIR + r"\certificates"

debounce_timer = None

def run_update():
    print("Updating gallery...")
    # 1. Regenerate thumbnails + index.html
    subprocess.run(["python", BASE_DIR + r"\script.py"])
    
    # 2. Git commit + push
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=BASE_DIR)
        commit_msg = "Auto update gallery"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd=BASE_DIR)
        subprocess.run(["git", "push"], check=True, cwd=BASE_DIR)
        print("Changes pushed to GitHub.")
    except subprocess.CalledProcessError:
        print("No changes to commit or push.")

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        global debounce_timer
        if event.is_directory:
            return
        # Debounce to wait for file operations to complete
        if debounce_timer:
            debounce_timer.cancel()
        debounce_timer = threading.Timer(1.5, run_update)
        debounce_timer.start()

observer = Observer()
observer.schedule(Handler(), CERT_DIR, recursive=False)
observer.start()

print("Watcher running...")

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    observer.stop()

observer.join()