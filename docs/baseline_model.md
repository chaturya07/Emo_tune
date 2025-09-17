# Baseline Model Design

- Labels: angry (includes disgust), fear, happy, neutral, sad, surprise  (6 classes)
- Input: grayscale, 48 x 48, single-channel, pixel values normalized to [0,1]
- Data: ml/data/processed/fer2013/{train,val,test}/{class}/
- Batch size: 32
- Loss: sparse_categorical_crossentropy
- Optimizer: Adam (lr=0.001)
- Initial epochs: 20 (sanity check 1-2 epochs)
- Metrics: accuracy, per-class precision/recall/F1, confusion matrix
- Model save path pattern: models/baseline_v{N}.h5
- Logs: logs/baseline_v{N}/tensorboard
- Metrics file: metrics/baseline_v{N}_metrics.csv
## Folder & File Conventions

- Models (checkpoints): models/baseline_v{N}/baseline_v{epoch:02d}.h5
- Final trained model: models/baseline_v{N}/baseline_final.h5
- TensorBoard logs: logs/baseline_v{N}/
- Evaluation metrics: metrics/baseline_v{N}/classification_report.json
- Confusion matrix plot: metrics/baseline_v{N}/confusion_matrix.png

> Note: Replace {N} with version number of the run.
## GitHub Commit Guidelines

**Commit:** ml/scripts/*.py, docs/baseline_model.md, other docs  
**Do NOT commit:** ml/data/raw/*, venv/, large models, logs/  
## Evaluation Metrics

- Overall Accuracy: from Keras evaluation on test set
- Per-class Precision, Recall, F1: from `classification_report.json`
- Confusion Matrix: plotted as `confusion_matrix.png`
- Optional: macro-F1 and weighted-F1 for overall assessment
