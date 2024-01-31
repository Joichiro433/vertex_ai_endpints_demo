"""
$ uvicorn main:app --reload
"""

import os
from enum import Enum

from rich import print
import numpy as np
import pandas as pd
import polars as pl
import lightgbm as lgb
from fastapi import FastAPI
from pydantic import BaseModel


# AIP_STORAGE_URI = os.environ.get('AIP_STORAGE_URI')
# AIP_HTTP_PORT = os.environ.get('AIP_HTTP_PORT', '80')
AIP_HEALTH_ROUTE = os.environ.get('AIP_HEALTH_ROUTE', '/health')
AIP_PREDICT_ROUTE = os.environ.get('AIP_PREDICT_ROUTE', '/predict')

app = FastAPI()
model = lgb.Booster(model_file='model.lgb')


class Specie(Enum):
    ADELIE = 0
    CHINSTRAP = 1
    GENTOO = 2


class PenguinFeature(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float


class Parameters(BaseModel):
    return_confidence: bool

    
class Prediction(BaseModel):
    specie: str
    confidence: float | None


class Predictions(BaseModel):
    predictions: list[Prediction]


@app.get(AIP_HEALTH_ROUTE, status_code=200)
async def health():
    return {'health': 'ok'}


@app.post(AIP_PREDICT_ROUTE, response_model=Predictions, response_model_exclude_unset=True)
async def predict(
        instances: list[PenguinFeature],
        parameters: Parameters | None = None,
    ) -> Predictions:
    """
    Make a prediction using the trained LightGBM model.

    This function takes a list of instances and optional parameters as input,
    converts the instances to a DataFrame, makes a prediction using the trained model,
    and returns the predictions along with optional confidence scores.

    Parameters
    ----------
    **instances** : list[PenguinFeature], [body parameter]\n
        A list of instances where each instance is a dictionary containing the features
        of a penguin. Each dictionary must have the following keys: 'bill_length_mm',
        'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'.
    **parameters** : Parameters, optional, [body parameter]\n
        An optional dictionary containing parameters for the prediction. Currently, the
        only supported parameter is 'return_confidence', which if set to True, will
        return the confidence score along with the prediction.

    Returns
    -------
    **Predictions**\n
        A Predictions object containing a list of Prediction objects. Each Prediction
        object contains the predicted species and an optional confidence score.
    """
    df_instance = pl.DataFrame(instances)
    preds = model.predict(df_instance.to_pandas())

    indices = np.argmax(preds, axis=-1)
    confidences = np.max(preds, axis=-1)

    if parameters is not None:
        return_confidence = parameters.return_confidence
    else:
        return_confidence = False

    outputs = []
    for index, confidence in zip(indices, confidences):
        specie = Specie(index).name
        if return_confidence:
            outputs.append(Prediction(specie=specie, confidence=confidence))
        else:
            outputs.append(Prediction(specie=specie))
            
    return Predictions(predictions=outputs)
