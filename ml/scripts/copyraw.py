import os
import shutil

# Paths
RAW_DIR = "ml/data/raw/fer2013"
PROCESSED_DIR = "ml/data/processed/fer2013"

# Folders to copy
folders_to_copy = ["train", "test"]

for folder in folders_to_copy:
    src = os.path.join(RAW_DIR, folder)
    dst = os.path.join(PROCESSED_DIR, folder)

    if not os.path.exists(src):
        print(f"⚠️ Source folder not found: {src}")
        continue

    # If processed folder already exists, skip (or you can clear it)
    if os.path.exists(dst):
        print(f"ℹ️ Skipping {folder}, already exists.")
        continue

    print(f"📂 Copying {folder} from {src} → {dst}")
    shutil.copytree(src, dst)

print("✅ Finished copying raw train & test data into processed folder.")
