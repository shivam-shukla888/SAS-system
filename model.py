import tensorflow as tf
from tensorflow.keras import layers, Model

def build_model(vocab_size):
    inp = layers.Input(shape=(32,256,1))
    labels = layers.Input(shape=(None,))
    input_len = layers.Input(shape=(1,))
    label_len = layers.Input(shape=(1,))

    x = layers.Conv2D(64,3,padding="same",activation="relu")(inp)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(128,3,padding="same",activation="relu")(x)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(256,3,padding="same",activation="relu")(x)

    shape = x.shape
    x = layers.Reshape((shape[2], shape[1]*shape[3]))(x)

    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)

    y_pred = layers.Dense(vocab_size + 1, activation="softmax")(x)  # +1 for blank

    loss = layers.Lambda(lambda args: tf.keras.backend.ctc_batch_cost(*args))(
        [labels, y_pred, input_len, label_len]
    )

    model = Model(
    inputs=[inp, labels, input_len, label_len],
    outputs=loss
    )
    model.compile(
    optimizer="adam",
    loss=lambda y_true, y_pred: y_pred
    )

    return model