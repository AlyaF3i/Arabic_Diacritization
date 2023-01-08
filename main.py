import os
import torch
import numpy as np
import tensorflow as tf
from Preprocess import Preprocess

from Decoder import Decoder

MODEL_FOLDER = os.path.abspath(os.path.join(__file__, os.pardir,"MODEL"))
#print(MODEL_FOLDER)
model_file = os.path.join(MODEL_FOLDER, "model.pt")
#print(model_file)
#exit()
model = torch.load(model_file)

def diacritize(input_text):
    diacritized_output = [""]
    processed_line = pre.prepare_text(input_text)
    predicted_line = model.predict(processed_line)
    predict_argmaxed = np.argmax(predicted_line,axis=2)
    decoded_line = decoder.decode(processed_line, predict_argmaxed)
    return decoded_line


if __name__ == '__main__':
    undiacritized_text = "السلام عليكم"
    diacritized_text = diacritize()
    print(diacritized_text)