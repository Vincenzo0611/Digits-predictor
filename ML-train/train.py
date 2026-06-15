import os
import pandas as pd
import numpy as np

from PIL import Image

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping


TRAIN_DIR = "./Digits/train"
VAL_DIR = "./Digits/val"
TEST_DIR = "./Digits/test"

def load_split(split_dir, image_size=(100, 100)):
    images = []
    labels = []

    for folder in os.listdir(split_dir):
        folder_path = os.path.join(split_dir, folder)

        if not os.path.isdir(folder_path):
            continue

        csv_path = os.path.join(folder_path, "labels.csv")

        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            image_name = row["image"]
            label = row["label"]

            image_path = os.path.join(folder_path, image_name)
            print(image_path)
            img = Image.open(image_path).convert("L")
            img = img.resize(image_size)

            img_array = np.array(img) / 255.0

            images.append(img_array)
            labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    return images, labels



X_train, y_train = load_split(TRAIN_DIR)
X_val, y_val = load_split(VAL_DIR)
X_test, y_test = load_split(TEST_DIR)

X_train = X_train[..., np.newaxis]
X_val = X_val[..., np.newaxis]
X_test = X_test[..., np.newaxis]

print(X_train.shape)
print(y_train.shape)


data_augmentation = tf.keras.Sequential([
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomTranslation(0.1, 0.1),
])

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)


model = models.Sequential([
    layers.Input(shape=(100, 100, 1)),

    data_augmentation,

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),

    layers.Dense(10, activation='softmax')
])


model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=[early_stop]
)

test_loss, test_acc = model.evaluate(X_test, y_test)

print("Test accuracy:", test_acc)


model.save("digit_model.keras")
