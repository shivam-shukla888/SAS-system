import cv2, numpy as np, pickle, tensorflow as tf
from tensorflow.keras.models import load_model
from preprocess import preprocess, resize
from segment import crop_line

model = load_model("outputs/handwriting_recognition.h5", compile=False)
vocab, idx_to_char = pickle.load(open("outputs/character_map.pkl","rb"))

def decode(pred):
    input_len = np.ones(pred.shape[0])*pred.shape[1]
    decoded = tf.keras.backend.ctc_decode(pred, input_length=input_len)[0][0]

    return "".join([idx_to_char.get(int(i),"") for i in decoded[0].numpy() if i!=-1])


def predict(image_path, polygon):
    img = cv2.imread(image_path)

    line = crop_line(img, polygon)
    line = preprocess(line)
    line = resize(line)

    line = np.expand_dims(line, axis=(0,-1))

    pred = model.predict(line)

    return decode(pred)