import os
from collections import Counter

# Base path to the processed dataset
base_path = "ml/data/processed/fer2013"

# Define the dataset splits to iterate through
splits = ["train", "val", "test"]

# Loop through each split folder
for split in splits:
    split_path = os.path.join(base_path, split)  # Full path to the current split
    class_counts = {}  # Dictionary to store number of images per class

    # Loop through each class folder within the split
    for emotion_class in os.listdir(split_path):
        class_folder = os.path.join(split_path, emotion_class)
        
        # Ensure it is a directory before counting files
        if os.path.isdir(class_folder):
            class_counts[emotion_class] = len(os.listdir(class_folder))

    # Calculate the total number of images in the split
    total = sum(class_counts.values())

    # Print the split name and total image count
    print(f"\n{split.upper()} ({total} images)")

    # Print the count and percentage of images for each class, sorted alphabetically
    for cls, count in sorted(class_counts.items()):
        print(f"{cls:<10}: {count} ({count/total:.2%})")
