import cv2
import numpy as np

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    thresh = cv2.adaptiveThreshold(
        gray,255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,2
    )
    return thresh


def resize(img):
    h, w = img.shape
    scale = 32/h
    new_w = int(w*scale)

    img = cv2.resize(img, (new_w,32))

    padded = 255*np.ones((32,256))
    padded[:, :min(new_w,256)] = img[:, :256]

    return padded/255.0