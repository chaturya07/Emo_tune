# Dataset Documentation

## Dataset Name
FER2013 (Facial Expression Recognition 2013)

## Source
[Kaggle - FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)

## License
- The dataset is distributed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- It can be used for research and educational purposes.

## Description
- FER2013 is a dataset of 35,887 grayscale facial images, each of size 48×48 pixels.
- Each image is labeled with one of seven emotions:
  - Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

## Why We Chose This Dataset
- It is a **standard benchmark** for facial emotion recognition.
- Large enough to train deep learning models.
- Already pre-cropped to faces, reducing preprocessing effort.
- Easy to download and reproducible by other team members.

## Preprocessing Plan
- Convert to grayscale (dataset already grayscale, so just verify).
- Normalize pixel values to [0, 1].
- Resize to 48×48 (already 48×48, so just confirm).
- Augment training data with small rotations, shifts, zoom, and flips.
- Split into train (70%), validation (15%), and test (15%) in a stratified way.
