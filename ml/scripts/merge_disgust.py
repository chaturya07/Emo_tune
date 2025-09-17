# ml/scripts/merge_disgust.py
import shutil
from pathlib import Path

# Define the base path for the processed FER2013 dataset
base = Path("ml/data/processed/fer2013")

# Iterate through each dataset split (train, validation, test)
for split in ["train", "val", "test"]:
    disgust_dir = base / split / "disgust"  # Path to "disgust" class folder
    angry_dir = base / split / "angry"      # Path to "angry" class folder

    if disgust_dir.exists():
        # Ensure "angry" folder exists; create it if missing
        angry_dir.mkdir(parents=True, exist_ok=True)
        moved = 0  # Counter to track number of moved files

        # Move all files from "disgust" to "angry"
        for f in disgust_dir.iterdir():
            if f.is_file():
                shutil.move(str(f), angry_dir / f.name)
                moved += 1

        # Attempt to remove the empty "disgust" folder after moving files
        try:
            disgust_dir.rmdir()
        except OSError:
            # Ignore errors if folder is not empty or cannot be removed
            pass

        # Log how many files were moved for this split
        print(f"Moved {moved} files from {disgust_dir} -> {angry_dir}")
    else:
        # If no disgust folder exists in this split, log that information
        print(f"No disgust folder in {split}")
