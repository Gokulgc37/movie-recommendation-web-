from fastapi import FastAPI , Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to your templates directory
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Load the pre-trained model
model = joblib.load("random_forest_best_model.pkl")

# Define the data model for prediction
class WineInput(BaseModel):
    feature_1: float
    feature_2: float
    feature_3: float
    feature_4: float
    feature_5: float
    feature_6: float
    feature_7: float
    feature_8: float
    feature_9: float
    feature_10: float
    feature_11: float

    # Add all relevant features

import logging

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(input_data : WineInput):
    data = np.array([[input_data.feature_1, input_data.feature_2, input_data.feature_3, input_data.feature_4, input_data.feature_5, input_data.feature_6, input_data.feature_7, input_data.feature_8, input_data.feature_9, input_data.feature_10, input_data.feature_11]])  # Include all features
    
    prediction = model.predict(data)

    if prediction[0] == 0:
        message = 'The wine quality is not good'
    else:
        message = 'The wine quality is good'
    
    return {"prediction": message}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

