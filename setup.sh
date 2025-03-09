#!/bin/bash

# 更新系統包管理器並安裝必要工具
apt-get update && apt-get install -y wget unzip

# 安裝 Google Chrome 瀏覽器
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# 獲取 Chrome 的主版本
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)

# 下載對應版本的 ChromeDriver
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip
if [ -f chromedriver_linux64.zip ]; then
    unzip chromedriver_linux64.zip -d /usr/local/bin/
    rm chromedriver_linux64.zip
else
    echo "ChromeDriver download failed"
    exit 1
fi
