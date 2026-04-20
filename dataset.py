import json
import cv2
import numpy as np
from segment import crop_line
from preprocess import preprocess, resize


# ===============================
# Load Data
# ===============================
def load_data():
    with open("data/annotations.json") as f:
        return json.load(f)


# ===============================
# Encode Text
# ===============================
def encode(text, vocab):
    return [vocab[c] for c in text if c in vocab]


# ===============================
# Data Generator (FIXED)
# ===============================
def generator(data, vocab, batch=8):
    while True:
        np.random.shuffle(data)

        for i in range(0, len(data), batch):
            batch_data = data[i:i+batch]

            imgs = []
            labels = []

            for item in batch_data:
                img = cv2.imread(f"data/images/{item['image']}")

                if img is None:
                    print("❌ Image not found:", item["image"])
                    continue

                line = crop_line(img, item["polygon"])

                if line is None:
                    print("❌ Crop failed")
                    continue

                try:
                    line = preprocess(line)
                    line = resize(line)
                except Exception as e:
                    print("❌ Preprocess error:", e)
                    continue

                imgs.append(line[..., None])
                labels.append(encode(item["text"], vocab))

            # 🚨 CRITICAL FIX
            if len(imgs) == 0:
                continue

            imgs = np.array(imgs)

            max_len = max(len(l) for l in labels)
            padded = np.zeros((len(labels), max_len))

            for j, l in enumerate(labels):
                padded[j, :len(l)] = l

            input_len = np.ones((len(imgs), 1)) * (256 // 4)
            label_len = np.array([[len(l)] for l in labels])

            yield (imgs, padded, input_len, label_len), np.zeros(len(imgs))