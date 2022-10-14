# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020
@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from bankcustomers import bank_customer
from applicant import applicant
import numpy as np
import pickle
import pandas as pd
import joblib

# 2. Create the app object
app = FastAPI()
pickle_in = open("model/best_LGB_10k_Undersampled_BestParams_Top5Features.pkl","rb")
model=pickle.load(pickle_in)

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_banknote(data:bank_customer):
    data = data.dict()
    variance=data['param1']
    skewness=data['param2']
    curtosis=data['param3']
    entropy=data['param4']
    # prediction = classifier.predict([[variance,skewness,curtosis,entropy]])
    prediction = variance + skewness + curtosis + entropy
    if(prediction>5):
        prediction="Fake note"
    else:
        prediction="Its a Bank note"
    return {
        'prediction': prediction
    }

@app.post('/preddefault')
def predict_default(data:applicant):
    data = data.dict()
    EXT_SOURCE_2=data['EXT_SOURCE_2']
    EXT_SOURCE_3=data['EXT_SOURCE_3']
    PAYMENT_RATE=data['PAYMENT_RATE']
    PrLI_DELAY_DAYS=data['PrLI_DELAY_DAYS']
    CODE_GENDER_F=data['CODE_GENDER_F']

    model = joblib.load('model/best_LGB_10k_Undersampled_BestParams_Top5Features.pkl')
    client = np.array([EXT_SOURCE_2,EXT_SOURCE_3,PAYMENT_RATE,PrLI_DELAY_DAYS,CODE_GENDER_F]).reshape(1, -1)
    probs = model.predict_proba(client)
    default_proba = probs[0][1]
    return {
        'prediction': default_proba
    }


# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload