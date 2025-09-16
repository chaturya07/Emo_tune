import os
from collections import Counter

# Adjust path if needed
base_path = "ml/data/processed/fer2013"

splits = ["train", "val", "test"]

for split in splits:
    split_path = os.path.join(base_path, split)
    class_counts = {}
    for emotion_class in os.listdir(split_path):
        class_folder = os.path.join(split_path, emotion_class)
        if os.path.isdir(class_folder):
            class_counts[emotion_class] = len(os.listdir(class_folder))

    total = sum(class_counts.values())
    print(f"\n📊 {split.upper()} ({total} images)")
    for cls, count in sorted(class_counts.items()):
        print(f"{cls:<10}: {count} ({count/total:.2%})")
