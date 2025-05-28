# Basic Ransomware Protection

A simple Python project that watches a folder in real-time to detect suspicious file activity, backs up files before changes, checks file integrity, and flags potentially ransomware-encrypted files by analyzing their entropy.

---

## How It Works

1. **Folder Monitoring:**  
   The script continuously watches a specific folder (`watched_folder`) for any file changes — creations, modifications, or deletions.

2. **Backup:**  
   Before a file is modified, it automatically creates a backup copy to a safe location (`backup/`).

3. **File Integrity Check:**  
   It calculates the SHA256 hash of every file and keeps track of these hashes in `file_hashes.txt` to detect if any file has been tampered with.

4. **Entropy Analysis:**  
   It calculates the Shannon entropy of files to estimate their randomness. High entropy usually means the file is encrypted or compressed — a common ransomware behavior. If the entropy is suspiciously high, the file gets quarantined for further inspection.

5. **Logging:**  
   All important actions and alerts are logged with timestamps, so you can review what happened.

---

## How to Run this shit

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/macOS
   venv\Scripts\activate      # On Windows

3. **Install dependencies:**
 
  ```bash
  pip3 install -r requirements.txt


4. **Start the watcher:**
 
  ```bash
   python3 watcher.py

