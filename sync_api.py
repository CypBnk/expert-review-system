import shutil
import os
import hashlib

SOURCE = os.path.join('self-hosted', 'backend', 'api_server.py')
DEST = 'api_server.py'

def get_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def sync():
    if not os.path.exists(SOURCE):
        print(f"Error: Source file '{SOURCE}' not found.")
        return

    source_hash = get_file_hash(SOURCE)
    dest_hash = get_file_hash(DEST)

    if source_hash != dest_hash:
        print(f"Syncing {SOURCE} -> {DEST}...")
        try:
            shutil.copy2(SOURCE, DEST)
            print("Sync complete.")
        except Exception as e:
            print(f"Error syncing file: {e}")
    else:
        print("Files are already in sync.")

if __name__ == "__main__":
    sync()
