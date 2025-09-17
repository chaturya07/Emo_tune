# ml/scripts/merge_disgust.py
import shutil
from pathlib import Path

base = Path("ml/data/processed/fer2013")
for split in ["train", "val", "test"]:
    disgust_dir = base / split / "disgust"
    angry_dir = base / split / "angry"
    if disgust_dir.exists():
        angry_dir.mkdir(parents=True, exist_ok=True)
        moved = 0
        for f in disgust_dir.iterdir():
            if f.is_file():
                shutil.move(str(f), angry_dir / f.name)
                moved += 1
        # remove empty folder if you want
        try:
            disgust_dir.rmdir()
        except OSError:
            pass
        print(f"Moved {moved} files from {disgust_dir} -> {angry_dir}")
    else:
        print(f"No disgust folder in {split}")
