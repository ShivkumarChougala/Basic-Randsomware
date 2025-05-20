import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDER = "watched_folder"
QUARANTINE_FOLDER = "quarantine"
BACKUP_FOLDER = "backup"

def log_event(event_type, message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {event_type}: {message}")

def backup_file(file_path):
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    filename = os.path.basename(file_path)
    backup_path = os.path.join(BACKUP_FOLDER, filename)
    shutil.copy2(file_path, backup_path)
    log_event("BACKUP", f"Backed up new file: {filename}")

def quarantine_file(file_path):
    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)
    filename = os.path.basename(file_path)
    quarantine_path = os.path.join(QUARANTINE_FOLDER, filename)
    shutil.move(file_path, quarantine_path)
    log_event("QUARANTINED", f"Quarantined suspicious file: {filename}")

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        log_event("CREATED", event.src_path)
        backup_file(event.src_path)
        quarantine_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        log_event("MODIFIED", event.src_path)

        # Phase 4: Detect if the decoy is touched
        if filename == '.DO_NOT_TOUCH.txt':
            log_event("ALERT", f"🚨 Decoy file modified! Possible ransomware activity.")

if __name__ == "__main__":
    print(f"🛡️ Monitoring '{WATCHED_FOLDER}' for changes... (Press Ctrl+C to stop)")
    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

