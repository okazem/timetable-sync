import os
import uvicorn
import json
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = 'credentials.json'
REDIRECT_URI = 'http://localhost:8000/auth'

app = FastAPI()

origins = [
    "http://localhost:5173",  # React(Vite)のデフォルトポート
    "http://localhost:3000",  # 一般的なReactのポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key='secret-key')

@app.get('/')
def index():
    return "<url>test</url>"

@app.get("/login")
def login(request: Request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    # セッションにstateを保存
    request.session['state'] = state
    return RedirectResponse(authorization_url)

@app.get("/auth")
def auth(request: Request):
    state = request.session.get('state')
    if not state:
        raise HTTPException(status_code=400, detail="State missing in session")

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state # stateを渡して検証
    )

    # 認可コードからトークンを取得
    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {e}")

    credentials = flow.credentials

    if credentials.refresh_token == None:
        return HTTPException(status_code=400, detail=f"")

    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    return {"message": "ログインに成功しました。カレンダー操作が可能です。"}