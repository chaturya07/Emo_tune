# ml/scripts/evaluate_baseline.py
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

def evaluate(model_path, data_dir, out_dir="metrics"):
    model = tf.keras.models.load_model(model_path)
    test_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "test"),
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        image_size=(48,48),
        batch_size=32,
        shuffle=False
    )
    class_names = test_ds.class_names
    y_true = []
    y_pred = []
    for x, y in test_ds:
        preds = model.predict(x)
        preds = np.argmax(preds, axis=1)
        y_pred.extend(preds.tolist())
        y_true.extend(y.numpy().tolist())

    report = classification_report(y_true, y_pred, target_names=class_names, digits=4, output_dict=True)
    print(classification_report(y_true, y_pred, target_names=class_names))
    cm = confusion_matrix(y_true, y_pred)
    os.makedirs(out_dir, exist_ok=True)
    # save report as txt or json
    import json
    with open(os.path.join(out_dir, "classification_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    # plot confusion matrix
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=class_names, yticklabels=class_names)
    plt.ylabel("True")
    plt.xlabel("Predicted")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "confusion_matrix.png"))
    print("Saved metrics to", out_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--data_dir", default="ml/data/processed/fer2013")
    parser.add_argument("--out_dir", default="metrics")
    args = parser.parse_args()
    evaluate(args.model, args.data_dir, args.out_dir)
