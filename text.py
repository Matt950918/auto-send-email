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

# 配置 Chrome 瀏覽器選項
chrome_options = Options()
chrome_options.add_argument("--headless")  # 無頭模式
chrome_options.add_argument("--disable-gpu")  # 停用 GPU
chrome_options.add_argument("--no-sandbox")  # 避免沙盒模式
chrome_options.add_argument("--disable-dev-shm-usage")  # 防止共享內存問題

# 使用 Selenium Manager 自動管理 ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# 登錄 Gmail
try:
    print("啟動瀏覽器，進入 Gmail 登錄頁面")
    driver.get("https://mail.google.com/")
    time.sleep(5)

    # 輸入用戶名
    driver.find_element(By.ID, "identifierId").send_keys(USERNAME)
    driver.find_element(By.ID, "identifierId").send_keys(Keys.RETURN)
    time.sleep(10)

    # 輸入密碼
    driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
    driver.find_element(By.NAME, "Passwd").send_keys(Keys.RETURN)
    time.sleep(20)

    # 檢查是否需要進行挑戰驗證
    if "challenge" in driver.current_url:
        print("需要進行驗證，請手動完成驗證。")
        time.sleep(30)

    # 點擊撰寫按鈕
    compose = driver.find_element(By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
    compose.click()
    time.sleep(5)

    # 發送消息給每位收件人
    for student_grade in range(int(grade_start), int(grade_end) + 1):
        for student_id in range(int(id_start), int(id_end) + 1):
            gmail_out = student_grade * (10**grade_len) + student_id
            print(f"發送郵件到: {first}{gmail_out}{address}")
            to_field = driver.find_element(By.CSS_SELECTOR, "textarea[name='to']")
            to_field.send_keys(f"{first}{gmail_out}{address}")
            to_field.send_keys(Keys.ENTER)
            time.sleep(3)

    # 輸入主題
    subject_field = driver.find_element(By.NAME, "subjectbox")
    subject_field.send_keys(topic)
    time.sleep(5)

    # 輸入郵件內容
    message_body = driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW")
    message_body.send_keys(MESSAGE)
    time.sleep(5)

    # 點擊發送按鈕
    send_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Send ‪(Ctrl-Enter)‬']")
    send_button.click()
    time.sleep(5)

    print("所有郵件已發送完成！")
except Exception as e:
    print(f"發送過程中出現錯誤: {e}")
finally:
    driver.quit()
    print("瀏覽器已關閉")
