# scripts/train_model_m2.py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os

# ---------------------------
# 1. Load Dataset
# ---------------------------
BATCH_SIZE = 32
IMG_SIZE = (224, 224)  # ResNet50 expects 224x224 RGB

train_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\admin\Emo_tune\ml\data\processed\fer2013\train",
    color_mode="rgb",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\admin\Emo_tune\ml\data\processed\fer2013\val",
    color_mode="rgb",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\admin\Emo_tune\ml\data\processed\fer2013\test",
    color_mode="rgb",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# ✅ Save class names before mapping
class_names = train_ds.class_names
num_classes = len(class_names)

# ---------------------------
# 2. Preprocessing & Augmentation
# ---------------------------
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomBrightness(0.1),
    layers.RandomContrast(0.1)
])

AUTOTUNE = tf.data.AUTOTUNE

train_ds = (
    train_ds
    .map(lambda x, y: (x / 255.0, y))
    .cache()
    .shuffle(1000)
    .prefetch(AUTOTUNE)
)

val_ds = val_ds.map(lambda x, y: (x / 255.0, y)).cache().prefetch(AUTOTUNE)
test_ds = test_ds.map(lambda x, y: (x / 255.0, y)).cache().prefetch(AUTOTUNE)

# ---------------------------
# 3. Build Transfer Learning Model
# ---------------------------
base_model = keras.applications.ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze some layers (allow fine-tuning from middle onwards)
base_model.trainable = True
for layer in base_model.layers[:100]:  # freeze first 100 layers
    layer.trainable = False

# Build model
inputs = keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)  # apply augmentation inside model
x = keras.applications.resnet.preprocess_input(x)  # ResNet preprocessing
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = keras.Model(inputs, outputs)

# ---------------------------
# 4. Compile Model
# ---------------------------
model.compile(
    optimizer=keras.optimizers.Adam(1e-4),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ---------------------------
# 5. Train Model
# ---------------------------
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=15
)

# ---------------------------
# 6. Evaluate Model
# ---------------------------
test_loss, test_acc = model.evaluate(test_ds)
print("✅ Test accuracy:", test_acc)

# Confusion Matrix
y_true = np.concatenate([y for x, y in test_ds], axis=0)
y_pred = np.argmax(model.predict(test_ds), axis=1)

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues, xticks_rotation=45)
plt.show()

# ---------------------------
# 7. Plot Training Curves
# ---------------------------
plt.figure(figsize=(12, 5))

# Accuracy plot
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()

# Loss plot
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()

plt.show()

# ---------------------------
# 8. Save Model
# ---------------------------
os.makedirs("models", exist_ok=True)
model.save("models/emotion_resnet50.h5")
print("Model saved at models/emotion_resnet50.h5")
