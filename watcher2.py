import os
import time
import shutil
import hashlib
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDER = "watched_folder"
BACKUP_FOLDER = "backup"
QUARANTINE_FOLDER = "quarantine"
HASH_STORE_FILE = "file_hashes.txt"  # To persist hashes across restarts

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def calculate_entropy(data):
    import math
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = data.count(x) / len(data)
        entropy -= p_x * math.log2(p_x)
    return entropy

def sha256_hash(filepath):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing {filepath}: {e}")
        return None

def load_hashes():
    hashes = {}
    if os.path.exists(HASH_STORE_FILE):
        with open(HASH_STORE_FILE, "r") as f:
            for line in f:
                try:
                    path, filehash = line.strip().split("||")
                    hashes[path] = filehash
                except:
                    continue
    return hashes

def save_hashes(hashes):
    with open(HASH_STORE_FILE, "w") as f:
        for path, filehash in hashes.items():
            f.write(f"{path}||{filehash}\n")

class RansomwareWatcher(FileSystemEventHandler):
    def __init__(self):
        self.file_hashes = load_hashes()
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

    def backup_file(self, src_path):
        try:
            filename = os.path.basename(src_path)
            backup_path = os.path.join(BACKUP_FOLDER, filename)
            shutil.copy2(src_path, backup_path)
            logging.info(f"✅ Backed up file: {filename}")
        except Exception as e:
            logging.error(f"[ERROR] Backup failed for {src_path}: {e}")

    def quarantine_file(self, src_path):
        try:
            filename = os.path.basename(src_path)
            quarantine_path = os.path.join(QUARANTINE_FOLDER, filename)
            shutil.move(src_path, quarantine_path)
            logging.warning(f"[QUARANTINED] {filename}")
        except Exception as e:
            logging.error(f"[ERROR] Quarantine failed for {src_path}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        path = event.src_path
        filename = os.path.basename(path)
        logging.info(f"[CREATED] {path}")
        self.backup_file(path)

        # Calculate hash and store
        file_hash = sha256_hash(path)
        if file_hash:
            self.file_hashes[path] = file_hash
            save_hashes(self.file_hashes)

    def on_modified(self, event):
        if event.is_directory:
            return
        path = event.src_path
        filename = os.path.basename(path)
        logging.info(f"[MODIFIED] {path}")

        # Calculate entropy for Phase 6 logic (optional, can keep or remove)
        try:
            with open(path, "rb") as f:
                data = f.read()
            entropy = calculate_entropy(data)
            logging.info(f"⚠️ Entropy for {filename}: {entropy:.2f}")
        except Exception as e:
            logging.error(f"[ERROR] Could not calculate entropy for {path}: {e}")
            entropy = 0

        # Backup file first
        self.backup_file(path)

        # Check hash to detect tampering
        new_hash = sha256_hash(path)
        old_hash = self.file_hashes.get(path)

        if new_hash and old_hash and new_hash != old_hash:
            # File content changed unexpectedly
            logging.warning(f"⚠️ FILE TAMPERING DETECTED: {filename}")
            # Optional: quarantine or alert here
            # self.quarantine_file(path)
        elif new_hash and old_hash is None:
            # New file tracked
            logging.info(f"Tracking new file hash: {filename}")

        # Update stored hash
        if new_hash:
            self.file_hashes[path] = new_hash
            save_hashes(self.file_hashes)

    def on_deleted(self, event):
        if event.is_directory:
            return
        path = event.src_path
        logging.info(f"[DELETED] {path}")
        # Remove hash tracking on delete
        if path in self.file_hashes:
            del self.file_hashes[path]
            save_hashes(self.file_hashes)

if __name__ == "__main__":
    event_handler = RansomwareWatcher()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    logging.info(f"🛡️ Monitoring '{WATCHED_FOLDER}' for changes... (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

