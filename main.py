import io
import json
import os
from http.client import HTTPException

import pandas as pd
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

from Extensions.JsonReplace import LoadJson
from Request.Ticket import Ticket
from Extensions.Regex import RegexIntent

app = FastAPI()
load_dotenv()
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")

@app.post("/DeterminationOfIntent")
def DeterminationOfIntent(ticket: Ticket):
    subject = ticket.subject
    selectedIntent = RegexIntent(subject)
    return selectedIntent

@app.post("/UploadExcel")
async def UploadExcel(file: UploadFile = File(...)):
    try:
        request_mail = []
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        for index, row in df.iterrows():
            body = row['body']
            if pd.isna(body) or pd.isnull(body) or str.strip(body) == '':
                continue
            selectedIntent = RegexIntent(body)
            if selectedIntent["category"] == "Bilinmiyor":
                request_mail.append({"id" : row["id"], "body" : row["body"]})
            else:
                df.at[index,'label'] = selectedIntent["category"]
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        if len(request_mail) > 0:
            response =  requests.post(N8N_WEBHOOK_URL, json=request_mail)
            res_data = response.json()
            ai_list = res_data[0]["category"]
            final_results = LoadJson(ai_list)
            for item in final_results:
                df.at[item["id"], 'label'] = item["category"]
        output_path = os.path.join(OUTPUT_FOLDER, "Islenmis_Cikti.xlsx")
        df.to_excel(output_path)
        return {"status": "success","Data Count" : len(df),"Go To Ai" : len(request_mail)}
    except Exception as e:
        error = str(e)
        raise HTTPException(status_code=500, detail=error)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
