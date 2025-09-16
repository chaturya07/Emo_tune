# Dataset Report – FER2013 (Processed)

## 1. Overview
This report summarizes the processed dataset used for facial emotion recognition in Emo_tune.

- **Dataset:** FER2013  
- **Source:** [Kaggle – FER2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)  
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
- **Total Images:** **35,887** (48×48 grayscale)

---

## 2. Class Distribution (Post-Split)

| Emotion   | Train | Val | Test | Total | % of Total |
|----------|-------|-----|------|-------|-----------|
| Angry    | 3396  | 599 | 958  | 4953  | 13.8% |
| Disgust* | 371   | 65  | 111  | 547   | 1.5% |
| Fear     | 3483  | 614 | 1024 | 5121  | 14.3% |
| Happy    | 6133  | 1082| 1774 | 8989  | 25.1% |
| Neutral  | 4221  | 744 | 1233 | 6198  | 17.3% |
| Sad      | 4106  | 724 | 1247 | 6077  | 16.9% |
| Surprise | 2696  | 475 | 831  | 4002  | 11.2% |
| **Total**| **24406** | **4303** | **7178** | **35887** | **100%** |

> **Note:** *Disgust will be merged with Angry during training to address class imbalance.*

---

## 3. Split Ratios

- **Train:** 68.0%  
- **Validation:** 12.0%  
- **Test:** 20.0%  

Although slightly different from the ideal 70/15/15 split, the distribution is still representative and acceptable.

---

## 4. Preprocessing Summary

- Verified grayscale format (48×48)  
- Normalized pixel values to `[0, 1]`  
- Performed stratified splitting into train/val/test  
- Light augmentation planned for training set:
  - Small rotations  
  - Width/height shifts  
  - Zoom  
  - Horizontal flips  

---

## 5. Notes on Imbalance
- The **Disgust** class is significantly underrepresented (~1.5%).  
- To mitigate this:
  - Disgust is merged with Angry (creating a single "Angry" class).
  - Additional data augmentation will be applied to improve class balance.

---

## 6. Reproducibility
- **Raw data** kept in `ml/data/raw/fer2013/` (not committed to GitHub).
- **Processed data** organized in:
