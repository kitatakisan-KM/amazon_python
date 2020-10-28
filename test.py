import os
from selenium import webdriver
userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + userdata_dir)

driver = webdriver.Chrome(options=options)
