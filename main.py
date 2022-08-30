from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from datetime import datetime
import pytz


app = FastAPI()

origins = [
    "https://app.flutterflow.io/",
    "http://app.flutterflow.io/",
    # "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://raz-wr-dashboard.codemagic.app",
    "https://raz-wr-dashboard.codemagic.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetchData():
    recent = pd.read_csv(
        'https://raw.githubusercontent.com/drdevinhopkins/hourly-report/main/data/recent.csv')
    current = recent.iloc[0]
    updateTimestamp = current.ds
    tbs = round(current['Total Pod TBS']+current['Total Vertical TBS'])
    last24 = recent.head(24)['Total Inflow hrly'].sum()
    stretchers = current['Total Stretcher pts']
    occupancy = round(stretchers/53*100)
    if occupancy >= 150 or tbs >= 30:
        busy = 'MUCH BUSIER THAN USUAL'
    elif occupancy >= 100 or tbs >= 20:
        busy = 'BUSIER THAN USUAL'
    else:
        busy = 'BUSY'
    dateTimeObj = datetime.now(tz=pytz.timezone('America/Toronto'))
    currentTimestamp = dateTimeObj.strftime("%d/%m/%Y %H:%M:%S")
    message = {"message": {"currentTimestamp": currentTimestamp, "updateTimestamp": updateTimestamp,
                           "TBS": str(tbs), "last24": str(last24), "occupancy": str(occupancy)+'%', "busy": busy}}
    return message


@app.get("/")
def read_root():
    return fetchData()


# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}
