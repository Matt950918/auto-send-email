from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
import subprocess
import os

app = FastAPI()
# 設置範本目錄為 gmailcreate 文件夾內的 templates 目錄
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 檢查範本文件是否存在
template_path = os.path.join(os.path.dirname(__file__), "templates", "gmail.html")
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

    # 使用絕對路徑
    file_path = "C:\\Users\\USER\\Music\\Desktop\\gmailcreate\\text.py"
    result = subprocess.run(["python", file_path], capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)



    return {"status": "Email sending initiated"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
