from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware  # 新增這一行
import uvicorn
import subprocess
import os

app = FastAPI()

# 添加 CORS 支援
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者限制為您的前端域名，例如 "https://your-netlify-site.netlify.app"
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設置範本目錄
base_dir = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 檢查範本文件是否存在
template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
if os.path.exists(template_path):
    print("Template file exists")
else:
    print("Template file does not exist")

class EmailRequest(BaseModel):
    username: str
    password: str
    topic: str
    message: str
    first: str
    address: str
    grade_start: str
    grade_end: str
    id_start: str
    id_end: str

@app.get("/", response_class=HTMLResponse)
async def send_email_form(request: Request):
    print("Handling GET request for /send-email")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-email")
async def send_email(
    username: str = Form(...),
    password: str = Form(...),
    topic: str = Form(...),
    message: str = Form(...),
    first: str = Form(...),
    address: str = Form(...),
    grade_start: str = Form(...),
    grade_end: str = Form(...),
    id_start: str = Form(...),
    id_end: str = Form(...)
):
    email_info_path = os.path.join(base_dir, "email_info.txt")
    with open("email_info.txt", "w") as f:
        f.write(f"{username}\n")
        f.write(f"{password}\n")
        f.write(f"{topic}\n")
        f.write(f"{message}\n")
        f.write(f"{first}\n")
        f.write(f"{address}\n")
        f.write(f"{grade_start}\n")
        f.write(f"{grade_end}\n")
        f.write(f"{id_start}\n")
        f.write(f"{id_end}\n")

    # 動態生成 text.py 路徑
    script_path = os.path.join(base_dir, "text.py")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    # 打印執行結果到伺服器日誌
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    return {"status": "Email sending initiated", "stdout": result.stdout, "stderr": result.stderr}

try:
    if __name__ == "__main__":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
except Exception as e:
    print(f"An error occurred: {e}")

