from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

 # 載入環境變數
load_dotenv()
app = FastAPI()

# 允許所有來源（開發用，正式環境請設限）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 或填 ["http://localhost:3000"] 只允許你的前端
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 連接到 MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["mydb"]  # 你可以自訂資料庫名稱
users_collection = db["users"]

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if not re.match(r"^[a-zA-Z0-9_]{8,20}$", password):
        raise HTTPException(status_code=400, detail="Invalid password format")
    new_user = {"username": username, "password": password}
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}