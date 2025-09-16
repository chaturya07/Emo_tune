import os, shutil, random
from pathlib import Path

# Paths
train_dir = Path("ml/data/raw/fer2013/train")
val_dir = Path("ml/data/processed/fer2013/val")
val_dir.mkdir(parents=True, exist_ok=True)

for emotion_folder in train_dir.iterdir():
    if emotion_folder.is_dir():
        images = list(emotion_folder.glob("*.jpg"))
        random.shuffle(images)
        val_count = int(0.15 * len(images))

        # Create class folder inside val/
        (val_dir / emotion_folder.name).mkdir(parents=True, exist_ok=True)

        # Move 15% images
        for img in images[:val_count]:
            shutil.move(str(img), val_dir / emotion_folder.name / img.name)

print("✅ Validation split complete! 15% of training images moved to val/")
