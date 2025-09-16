import os

base_dir = "ml/data/processed/fer2013"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

def count_images(folder):
    count = 0
    for root, _, files in os.walk(folder):
        count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    return count

train_count = count_images(train_dir)
val_count = count_images(val_dir)
test_count = count_images(test_dir)

total = train_count + val_count + test_count

if total == 0:
    print("⚠️ No images found — check your folder paths or processed data!")
else:
    print(f"Train: {train_count} ({train_count/total:.2%})")
    print(f"Validate: {val_count} ({val_count/total:.2%})")
    print(f"Test: {test_count} ({test_count/total:.2%})")
    print(f"Total: {total}")
