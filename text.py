from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# 啟動 WebDriver
driver = webdriver.Chrome(executable_path=r"C:\Users\USER\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # 替換為你的 chromedriver 路徑
driver.get("https://mail.google.com/") 

# 等待頁面加載
time.sleep(5)

# 登入
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

# 發送消息給每位摯友
# 打開 DM (Direct Message) 頁面
compose = driver.find_element(By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
compose.click()
time.sleep(5)

# 輸入收件人
for student_grade in range(int(grade_start), int(grade_end)+1):
    for student_id in range(int(id_start), int(id_end)+1):
        gmail_out = student_grade * (10**grade_len) + student_id
        print(gmail_out)
        to_field = driver.find_element(By.CSS_SELECTOR, "input[aria-label='收件者']")
        to_field.send_keys(f"{first}{gmail_out}{address}")
        to_field.send_keys(Keys.ENTER)
        to_field.send_keys(" ")
        time.sleep(5)

# 輸入主題
subject_field = driver.find_element(By.NAME, "subjectbox")
subject_field.send_keys(topic)
time.sleep(5)

# 輸入訊息內容
message_body = driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW")
message_body.send_keys(MESSAGE)
time.sleep(5)

# 點擊發送按鈕
send_button = driver.find_element(By.CLASS_NAME, "T-I.J-J5-Ji.aoO.v7.T-I-atl.L3")
send_button.click()
time.sleep(5)
print("消息已發送完成！")
driver.quit()
