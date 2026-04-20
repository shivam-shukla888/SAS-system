import streamlit as st
import cv2
import numpy as np
import pickle
import tensorflow as tf

from preprocess import preprocess, resize


# =========================
# Load vocab
# =========================
data = pickle.load(open("outputs/character_map.pkl", "rb"))

if len(data) == 2:
    char_to_idx, idx_to_char = data
else:
    char_to_idx, idx_to_char, _ = data


# =========================
# Build inference model
# =========================
from tensorflow.keras import layers, Model

def build_inference_model(vocab_size):
    inp = layers.Input(shape=(32, 256, 1))

    x = layers.Conv2D(64, 3, padding="same", activation="relu")(inp)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(256, 3, padding="same", activation="relu")(x)

    shape = x.shape
    x = layers.Reshape((shape[2], shape[1] * shape[3]))(x)

    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)

    y_pred = layers.Dense(vocab_size + 1, activation="softmax")(x)

    return Model(inp, y_pred)


# =========================
# Load model weights
# =========================
model = build_inference_model(len(char_to_idx))
model.load_weights("outputs/handwriting_recognition.h5")


# =========================
# Decode (CTC)
# =========================
def decode(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]

    decoded = tf.keras.backend.ctc_decode(
        pred,
        input_length=input_len
    )[0][0]

    result = []
    for i in decoded[0].numpy():
        if i != -1:
            result.append(idx_to_char.get(int(i), ""))

    return "".join(result)


# =========================
# Predict
# =========================
def predict_line(img):
    try:
        img = preprocess(img)
        img = resize(img)

        img = np.expand_dims(img, axis=(0, -1))

        pred = model.predict(img, verbose=0)

        return decode(pred)

    except Exception as e:
        return f"Error: {e}"


# =========================
# UI
# =========================
st.title("✍️ Handwriting Recognition")

uploaded = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    st.image(img, caption="Uploaded Image", width="stretch")

    st.write("### Prediction:")

    text = predict_line(img)

    st.success(text)