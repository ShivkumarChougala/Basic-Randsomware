# backup.py

import os
import shutil
import hashlib

BACKUP_FOLDER = "backup"

def compute_hash(file_path):
    """Returns SHA256 hash of the file contents"""
    h = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def backup_file(file_path):
    """Backs up file if not already backed up or if it has changed"""
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        return

    rel_path = os.path.relpath(file_path, "watched_folder")
    backup_path = os.path.join(BACKUP_FOLDER, rel_path)

    os.makedirs(os.path.dirname(backup_path), exist_ok=True)

    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backed up new file: {rel_path}")
    else:
        original_hash = compute_hash(file_path)
        backup_hash = compute_hash(backup_path)
        if original_hash != backup_hash:
            shutil.copy2(file_path, backup_path)
            print(f"🔁 File updated, backup replaced: {rel_path}")

