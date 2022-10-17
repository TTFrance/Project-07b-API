# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020
@author: win10
"""

# Library imports
import uvicorn
from fastapi import FastAPI, HTTPException
import numpy as np
import pickle
import pandas as pd
import joblib

# Create the app object
app = FastAPI()
# load the model
model = joblib.load('model/best_LGB_10k_Undersampled_BestParams.pkl')
#load the X_train dataframe
df = pd.read_pickle('data/client_data_api_dashboard_1k.pkl')

# Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'OCP7API'}

@app.get('/predict/{SK_ID_CURR}')
def predict_default(SK_ID_CURR:int):
    if SK_ID_CURR in df.index:
        # retrieve client id from the GET
        client = df.loc[[SK_ID_CURR]].drop(columns=['TARGET'])
        # predict the class probabilities
        probs = model.predict_proba(client)
        # take the probability of credit default as the response (% chance to not repay loan)
        default_proba = probs[0][1]
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        'prediction': default_proba
    }

@app.get('/getids/{SK_ID_CURR}')
def getids():
    return df.index.values.tolist()

# Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# TO RUN THIS...
# cd C:\Users\adam_\Desktop\OC\Project 07\Project-07b-API
# uvicorn app:app --reload