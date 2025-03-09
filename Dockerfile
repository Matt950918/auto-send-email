# 使用 Python 官方基礎映像
FROM python:3.9-slim

# 確保最新的基礎映像
RUN apt-get update && apt-get upgrade -y

# 安裝必要工具和依賴（wget、unzip、gnupg 用於安裝 Chrome）
RUN apt-get install -y wget unzip gnupg

# 安裝 Google Chrome
RUN wget https://dl.google.com/linux/linux_signing_key.pub && \
    apt-key add linux_signing_key.pub && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# 獲取 Chrome 瀏覽器版本，並安裝對應版本的 ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# 設定工作目錄
WORKDIR /app

# 複製當前目錄下的所有檔案到容器內
COPY . .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 指定 Chrome binary 的位置，避免 WebDriver 無法找到 Chrome 的問題
ENV PATH="/usr/bin/google-chrome:$PATH"

# 指定啟動命令（執行您的 Python 腳本）
CMD ["python", "text.py"]
