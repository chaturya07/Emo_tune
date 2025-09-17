# ml/scripts/sanity_check.py
import tensorflow as tf
from tensorflow import keras
import os

def main():
    data_dir = "ml/data/processed/fer2013"
    batch = 32
    # use small subset by using image_dataset_from_directory's validation_split trick
    train_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "train"),
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        image_size=(48,48),
        batch_size=batch,
        shuffle=True
    )
    # take only small number of batches
    small_train = train_ds.take(4)  # ~4 * batch images
    val_ds = tf.keras.utils.image_dataset_from_directory(os.path.join(data_dir, "val"),
                                                         labels="inferred", label_mode="int",
                                                         color_mode="grayscale", image_size=(48,48),
                                                         batch_size=batch, shuffle=False).take(1)
    model = keras.Sequential([
        keras.layers.Input(shape=(48,48,1)),
        keras.layers.Rescaling(1./255),
        keras.layers.Conv2D(16,3, activation='relu'),
        keras.layers.MaxPool2D(),
        keras.layers.Flatten(),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(len(train_ds.class_names), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(small_train, validation_data=val_ds, epochs=1)
    print("Sanity check finished.")

if __name__ == "__main__":
    main()
