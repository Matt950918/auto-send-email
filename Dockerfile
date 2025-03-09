# 使用 Python 官方映像
FROM python:3.9-slim

# 安裝必要工具與 Chrome 瀏覽器
RUN apt-get update && apt-get install -y wget unzip gnupg && \
    wget https://dl.google.com/linux/linux_signing_key.pub && \
    apt-key add linux_signing_key.pub && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# 安裝與 Chrome 匹配的 ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# 安裝 Python 依賴
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 工作目錄與啟動命令
WORKDIR /app
COPY . /app
CMD ["python", "text.py"]
