# ml/scripts/train_baseline.py
import os
import argparse
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

AUTOTUNE = tf.data.AUTOTUNE

def build_model(input_shape=(48,48,1), num_classes=6):
    model = keras.Sequential([
        keras.layers.Input(shape=input_shape),
        keras.layers.Rescaling(1./255),
        
        keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
        keras.layers.MaxPooling2D(),
        keras.layers.BatchNormalization(),

        keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
        keras.layers.MaxPooling2D(),
        keras.layers.BatchNormalization(),

        keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
        keras.layers.MaxPooling2D(),
        keras.layers.BatchNormalization(),

        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    return model

def get_datasets(data_dir, batch_size):
    # Load train dataset
    train_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "train"),
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        image_size=(48,48),
        batch_size=batch_size,
        shuffle=True
    )
    # Get class names BEFORE caching/prefetch
    class_names = train_ds.class_names

    # Load validation dataset
    val_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "val"),
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        image_size=(48,48),
        batch_size=batch_size,
        shuffle=False
    )

    # Load test dataset
    test_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "test"),
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        image_size=(48,48),
        batch_size=batch_size,
        shuffle=False
    )

    # Performance optimization
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names

def main(args):
    data_dir = args.data_dir
    batch = args.batch_size
    epochs = args.epochs
    model_dir = Path(args.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    logs = Path(args.logs)
    logs.mkdir(parents=True, exist_ok=True)

    # Load datasets
    train_ds, val_ds, test_ds, class_names = get_datasets(data_dir, batch)
    num_classes = len(class_names)
    print("Classes:", class_names)

    model = build_model(input_shape=(48,48,1), num_classes=num_classes)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    # Callbacks
    ckpt = keras.callbacks.ModelCheckpoint(
        filepath=str(model_dir / "baseline_v{epoch:02d}.h5"),
        save_best_only=True,
        monitor="val_accuracy",
        mode="max"
    )
    tb = keras.callbacks.TensorBoard(log_dir=str(logs), histogram_freq=1)
    es = keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    # Train model
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[ckpt, tb, es]
    )

    # Save final model
    final_model_path = model_dir / "baseline_final.h5"
    model.save(final_model_path)
    print("✅ Training complete. Model saved to", final_model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="ml/data/processed/fer2013", help="Processed data directory")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--model_dir", default="models")
    parser.add_argument("--logs", default="logs/baseline")
    args = parser.parse_args()
    main(args)
