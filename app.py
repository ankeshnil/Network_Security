import os
import sys
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongodb_db_url = os.getenv("MONGO_DB_URL")
print(mongodb_db_url)

import pymongo
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import trainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form   # 🔧 UPDATED
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

# 🔥 NEW (feature extraction import)
from networksecurity.utils.feature_extraction import extract_features


# MongoDB connection
client = pymongo.MongoClient(mongodb_db_url, tls=True, tlsCAFile=ca)

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


# 🔥 NEW (Homepage UI)
@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Training route
@app.get("/train")
async def train_route():
    try:
        train_pipeline = trainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkException(e, sys)


# ---------------- OLD CSV PREDICTION ----------------
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)

        df['predicted_column'] = y_pred

        df.to_csv("prediction_output/output.csv")

        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html}
        )

    except Exception as e:
        raise NetworkException(e, sys)


# ---------------- 🔥 NEW URL PREDICTION ----------------
@app.post("/predict_form")
async def predict_form(request: Request):
    try:
        form = await request.form()
        url = form.get("url")

        if not url:
            return {"error": "URL is required"}

        # 🔥 Feature Extraction
        features = extract_features(url)

        # 🔥 IMPORTANT: maintain column order
        columns = [
        "having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol",
        "double_slash_redirecting","Prefix_Suffix","having_Sub_Domain",
        "SSLfinal_State","Domain_registeration_length","Favicon","port",
        "HTTPS_token","Request_URL","URL_of_Anchor","Links_in_tags","SFH",
        "Submitting_to_email","Abnormal_URL","Redirect","on_mouseover",
        "RightClick","popUpWidnow","Iframe","age_of_domain","DNSRecord",
        "web_traffic","Page_Rank","Google_Index","Links_pointing_to_page",
        "Statistical_report"
        ]

        df = pd.DataFrame([features])[columns]

        # 🔥 Load model
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor, model)

        prediction = network_model.predict(df)

        result = "Safe ✅" if prediction[0] == 1 else "Phishing ❌"

        # 🔥 OPTIONAL: Save to MongoDB
        collection.insert_one({
            "url": url,
            "features": features,
            "prediction": int(prediction[0])
        })

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "url": url, "result": result}
        )

    except Exception as e:
        return {"error": str(e)}


# Run app
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)