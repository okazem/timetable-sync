import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, UserToken
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from fastapi import Depends
from sqlalchemy.orm import Session 
from google.auth.transport import requests as google_requests

from database import UserToken

# 開発環境のみHTTPを許可 (本番では必ず削除またはFalseに)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = [
    "openid", 
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

CREDENTIALS_FILE = 'credentials.json'
REDIRECT_URI = 'http://localhost:8000/auth'
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

# DBセッションを取得するための関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS設定
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# セッション設定
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    same_site="lax", # ブラウザのCookie制限対策
    https_only=False  # 開発中のみFalse
)

@app.get("/login")
def login(request: Request):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    # prompt='consent' を入れることで、必ずリフレッシュトークンを発行させる
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent' 
    )
    request.session['state'] = state
    return RedirectResponse(authorization_url)

@app.get("/auth")
def auth(request: Request, db: Session = Depends(get_db)): # dbを注入
    state = request.session.get('state')
    if not state:
        raise HTTPException(status_code=400, detail="State missing in session")

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )

    try:
        # トークンを取得
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {e}")

    credentials = flow.credentials

    # --- 重要：GoogleからユーザーIDを取得する ---
    # id_tokenを検証して、ユーザー固有の識別子(sub)を取り出す
    try:
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, 
            google_requests.Request(), 
            credentials.client_id
        )
        google_user_id = id_info['sub'] # これをuser_idとして使う
        google_user_name = id_info['name']
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to parse user info")

    # DBに保存するオブジェクトを作成
    new_token = UserToken(
        user_id=google_user_id,
        user_name=google_user_name,
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes,
    )

    # DB保存処理
    db.merge(new_token)
    db.commit()

    request.session['user_id'] = google_user_id

    return RedirectResponse(url="http://localhost:8000/dashboard")

@app.get("/dashboard")
def dashboard(request: Request,db: Session = Depends(get_db)):

    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_info = db.query(UserToken).get(user_id)
    user_name = user_info.user_name

    