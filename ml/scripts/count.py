import os

# Base directory where the processed FER2013 dataset is stored
base_dir = "ml/data/processed/fer2013"

# Paths for each data split
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

def count_images(folder):
    """
    Counts the number of image files in a given folder (recursively).
    
    Only files with extensions .png, .jpg, and .jpeg are considered as images.
    """
    count = 0
    for root, _, files in os.walk(folder):
        # Filter files to include only image formats
        count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    return count

# Count the number of images in each split
train_count = count_images(train_dir)
val_count = count_images(val_dir)
test_count = count_images(test_dir)

# Calculate total images across all splits
total = train_count + val_count + test_count

# Display results or show warning if no images are found
if total == 0:
    print("No images found — check your folder paths or processed data!")
else:
    print(f"Train: {train_count} ({train_count/total:.2%})")
    print(f"Validate: {val_count} ({val_count/total:.2%})")
    print(f"Test: {test_count} ({test_count/total:.2%})")
    print(f"Total: {total}")
