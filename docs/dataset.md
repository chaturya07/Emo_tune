# Dataset Documentation

## Dataset Name
FER2013 (Facial Expression Recognition 2013)

## Source
[Kaggle - FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)

## License
- Distributed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- Free to use for research and educational purposes.

## Description
- FER2013 is a dataset of **35,887 grayscale facial images** (48×48 pixels each).
- Each image is labeled with one of seven emotions:
  - Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

## Why We Chose This Dataset
- Standard benchmark for facial emotion recognition.
- Large enough to train deep learning models.
- Already pre-cropped to faces (minimal preprocessing required).
- Easy to download and reproducible for all team members.

## Setup Instructions
- **Download:** From [Kaggle](https://www.kaggle.com/datasets/msambare/fer2013).
- **Extract & Place:**
  - Put the extracted folders under `ml/data/raw/fer2013/`
  - Final folder structure should look like:
    ```
    ml/
      data/
        raw/
          fer2013/
            train/
            test/
    ```
- **Important:**  
  - Do **NOT** commit raw dataset files to GitHub.  
  - Keep a `.gitkeep` file in `ml/data/raw/` so the folder exists in the repo.  
  - This prevents the repo from becoming too large and respects dataset licensing.

## Emotion Classes
We will use **6 classes** by merging "Disgust" into "Angry":
- Angry (includes Disgust)
- Fear
- Happy
- Sad
- Surprise
- Neutral

## Preprocessing Plan
- Verify grayscale format (dataset is already grayscale).
- Normalize pixel values to `[0, 1]`.
- Ensure all images are 48×48 (already correct).
- Apply **light data augmentation** on training set only:
  - Small rotations, shifts, zoom, horizontal flips.

## Dataset Split
- **Train:** 70%
- **Validation:** 15% (split from training set)
- **Test:** 15% (from provided test folder)
- Maintain stratification (equal class distribution across splits).

## Notes
- Class distribution will be documented after preprocessing.
- Any imbalances will be handled by augmentation or class weights during training.
## Class Distribution (after preprocessing)
| Emotion  | Count |
|---------|------|
| Angry   | TBD |
| Fear    | TBD |
| Happy   | TBD |
| Sad     | TBD |
| Surprise| TBD |
| Neutral | TBD |

> Will be updated after preprocessing is complete.
### Tools Used
- **Python 3.10+**
- **Libraries:** NumPy, Pandas, OpenCV, scikit-learn
- Preprocessing script will be stored in `ml/scripts/preprocess.py`

