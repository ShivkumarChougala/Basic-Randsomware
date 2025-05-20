import os
import shutil

WATCHED_FOLDER = "watched_folder"
BACKUP_FOLDER = "backup"

def recover_files():
    if not os.path.exists(BACKUP_FOLDER):
        print("No backup folder found. Nothing to recover.")
        return

    if not os.path.exists(WATCHED_FOLDER):
        os.makedirs(WATCHED_FOLDER)

    for filename in os.listdir(BACKUP_FOLDER):
        backup_file_path = os.path.join(BACKUP_FOLDER, filename)
        recover_path = os.path.join(WATCHED_FOLDER, filename)

        shutil.copy2(backup_file_path, recover_path)
        print(f"Recovered: {filename}")

    print("Recovery complete.")

if __name__ == "__main__":
    recover_files()

