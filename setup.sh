# 更新系統包管理器並安裝必要工具
apt-get update && apt-get install -y wget unzip

# 安裝 Google Chrome 瀏覽器
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# 獲取 Chrome 的主要版本並安裝對應版本的 ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/

# 清理下載的臨時文件
rm google-chrome-stable_current_amd64.deb chromedriver_linux64.zip
