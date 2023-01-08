import os
from typing import Optional, Dict
import tempfile
import torch
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from Preprocess import Preprocess

from Decoder import Decoder


MODEL_FOLDER = os.environ["MODEL_FOLDER"]
PORT = int(os.environ["PORT"])

class APIInput(BaseModel):
    data: str = ""
    language: str = ""
    dialect: Optional[str] = ""


class APIOutput(BaseModel):
    data: str = ""
    details: Dict = ""

app = FastAPI()

pre = Preprocess()
decoder = Decoder()

model_file = os.path.join(MODEL_FOLDER, "model.pt")
model = torch.load(model_file)

@app.post("/diacritize")
def diacritize(api_input: APIInput) -> APIOutput:
    diacritized_output = [""]
    processed_line = pre.prepare_text(api_input.data)
    predicted_line = model.predict(processed_line)
    predict_argmaxed = np.argmax(predicted_line,axis=2)
    decoded_line = decoder.decode(processed_line, predict_argmaxed)

    return APIOutput(**{
        "data": decoded_line,
        "details": {
            "text": decoded_line,
        }
    })

if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=PORT)
