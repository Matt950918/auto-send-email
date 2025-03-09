from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 讀取輸入資料
with open("email_info.txt", "r") as f:
    data = f.read().splitlines()

USERNAME = data[0]
PASSWORD = data[1]
topic = data[2]
MESSAGE = data[3]
first = data[4]
address = data[5]
grade_start = data[6]
grade_end = data[7]
id_start = data[8]
id_end = data[9]
grade_len = len(id_start)

# 設置 ChromeDriver 路徑和選項
chrome_driver_path = "/usr/local/bin/chromedriver"  # Render 上的預設安裝路徑
chrome_options = Options()
chrome_options.add_argument("--headless")  # 啟用無頭模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 啟動 WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 進入 Gmail 登錄頁面
driver.get("https://mail.google.com/")

# 等待頁面加載
time.sleep(5)

# 登入 Gmail
driver.find_element(By.ID, "identifierId").send_keys(USERNAME)
driver.find_element(By.ID, "identifierId").send_keys(Keys.RETURN)
time.sleep(10)
driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
driver.find_element(By.NAME, "Passwd").send_keys(Keys.RETURN)
time.sleep(20)

# 確保登入成功
if "challenge" in driver.current_url:
    print("需要進行驗證，請手動完成驗證。")
    time.sleep(30)

# 點擊撰寫郵件按鈕
compose = driver.find_element(By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
compose.click()
time.sleep(5)

# 輸入收件人
for student_grade in range(int(grade_start), int(grade_end)+1):
    for student_id in range(int(id_start), int(id_end)+1):
        gmail_out = student_grade * (10**grade_len) + student_id
        print(gmail_out)
        to_field = driver.find_element(By.CSS_SELECTOR, "textarea[name='to']")
        to_field.send_keys(f"{first}{gmail_out}{address}")
        to_field.send_keys(Keys.ENTER)
        time.sleep(3)

# 輸入主題
subject_field = driver.find_element(By.NAME, "subjectbox")
subject_field.send_keys(topic)
time.sleep(5)

# 輸入訊息內容
message_body = driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW")
message_body.send_keys(MESSAGE)
time.sleep(5)

# 點擊發送按鈕
send_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Send ‪(Ctrl-Enter)‬']")
send_button.click()
time.sleep(5)

print("消息已發送完成！")
driver.quit()
