"""Module for defining and training the classifier.
Commented lines represent different things tried during the project."""

import datetime
from typing import Tuple
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Model
from tensorflow.keras import callbacks
from tensorflow.keras import metrics
# from tensorflow.keras.appgit slications.mobilenet_v2 import MobileNetV2, preprocess_input
# from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.applications.resnet_v2 import ResNet152V2, preprocess_input
from tensorflow.keras.layers import Input, Dense, GlobalAveragePooling2D, \
    BatchNormalization, ReLU, LayerNormalization
from betel import classifier_sequence


def define_model() -> Tuple[Model, Model]:
    """Defines the architecture of the model."""
    i = Input([None, None, 3], dtype=tf.uint8)
    x = tf.cast(i, tf.float32)
    x = preprocess_input(x)

    # base_model = MobileNetV2(include_top=False, weights='imagenet', input_shape=(192, 192, 3))
    # base_model = ResNet50(include_top=False, weights='imagenet', input_shape=(192, 192, 3))
    base_model = ResNet152V2(include_top=False, weights='imagenet', input_shape=(192, 192, 3))
    x = base_model(x)

    x = GlobalAveragePooling2D()(x)
    x = Dense(512, kernel_regularizer='l2')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    # x = LayerNormalization()(x)
    # x = Dense(256, kernel_regularizer='l2')(x)
    # x = BatchNormalization()(x)
    # x = ReLU()(x)
    # x = LayerNormalization()(x)
    x = Dense(64, kernel_regularizer='l2')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    # x = LayerNormalization()(x)
    predictions = Dense(1, activation='sigmoid', kernel_regularizer='l2')(x)

    model = Model(inputs=[i], outputs=predictions)

    return model, base_model


def train_model(model: Model, base_model: Model, train_gen: classifier_sequence.ClassifierSequence,
                val_gen: classifier_sequence.ClassifierSequence) -> None:
    """Trains the model on the given data sets."""
    for layer in base_model.layers:
        layer.trainable = False

    opt = optimizers.SGD(learning_rate=0.00001, momentum=0.8, clipnorm=1)
    # opt = optimizers.Adam(learning_rate=0.000001)

    model.compile(optimizer=opt,
                  loss='binary_crossentropy',
                  metrics=['accuracy', metrics.Recall(),
                           metrics.Precision(), metrics.FalsePositives(),
                           metrics.FalseNegatives()])

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    model.fit(train_gen,
              validation_data=val_gen,
              epochs=60,
              callbacks=[tensorboard_callback])

    for layer in base_model.layers:
        layer.trainable = True

    opt = optimizers.SGD(learning_rate=0.00001, momentum=0.8, clipnorm=1)

    model.compile(optimizer=opt,
                  loss='binary_crossentropy',
                  metrics=['accuracy', metrics.Recall(),
                           metrics.Precision(), metrics.FalsePositives(),
                           metrics.FalseNegatives()])

    model.fit(train_gen,
              validation_data=val_gen,
              epochs=120,
              initial_epoch=60,
              callbacks=[tensorboard_callback])
