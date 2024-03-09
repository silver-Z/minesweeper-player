import os
import tensorflow as tf
import cv2
import numpy as np
import imutils
from imutils import contours
from skimage.segmentation import clear_border

__package__ = "digital_recognizer"

def extract_digit(cell, model):
    cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        return None
    
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    
    (h, w) = thresh.shape
    percentFilled = cv2.countNonZero(mask) / float(w * h)
    # if less than 3% of the mask is filled then we are looking at
    # noise and can safely ignore the contour
    if percentFilled < 0.03:
        return None
    
    # apply the mask to the thresholded cell
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)
    digit = cv2.resize(digit, (28, 28))

    return model.predict(digit.reshape(1, 28, 28, 1)).argmax(axis=1)


def load_model():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the model file
    model_path = os.path.join(script_dir, 'models', 'digit-recognizer.h5')

    # Load and return the model
    return tf.keras.models.load_model(model_path)