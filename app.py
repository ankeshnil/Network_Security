import os
import sys
import certifi
ca = certifi.where()

from dotenv  import load_dotenv
load_dotenv()
mongodb_db_url = os.getenv("MONGODB_URL_KEY")
print(mongodb_db_url)

import pymongo
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import trainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

import pandas as pd
import pymongo

from networksecurity.utils.main_utils.utils import load_object

# MongoDB connection
client = pymongo.MongoClient(mongodb_db_url, tlsCAFile=ca)

from networksecurity.constant.traning_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.traning_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

# Redirect to docs
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# Training route
@app.get("/train")
async def train_route():
    try:
        train_pipeline = trainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        # print(df)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)

        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        # df['predicted_column'].replace(-1, 0)
        # return df.to_json()
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes='table table-striped')
        # print(table_html)

        return templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html}
        )

    except Exception as e:
        raise NetworkException(e, sys)
    
    
if __name__ == "__main__":
    app_run(app, host="localhost", port= 8000)