from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1LA4keTLZrV3VuBi5dq66oUDiJzzICBuWFpaRhbIn54k'

def write_to_sheet(content):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    body = {
        'values': [[content]]
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="project!M:M",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    return result

@app.route("/generate", methods=["POST"])
def generate():
    generated_text = "무협 웹소설 자동 생성 예시입니다."
    try:
        write_to_sheet(generated_text)
        return jsonify({"result": generated_text, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
