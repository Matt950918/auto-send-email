# 使用 Python 官方基礎映像
FROM python:3.9-slim

# 更新並安裝必需的系統工具
RUN apt-get update && apt-get install -y wget unzip gnupg

# 安裝 Google Chrome
RUN wget https://dl.google.com/linux/linux_signing_key.pub && \
    apt-key add linux_signing_key.pub && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# 安裝與 Chrome 匹配的 ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# 設置工作目錄
WORKDIR /app

# 複製所有檔案到容器
COPY . .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變數來指定 Chrome 的執行檔案位置
ENV PATH="/usr/bin/google-chrome:$PATH"

# 啟動應用程式
CMD ["python", "text.py"]
