from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL")
COURSE_URL = os.getenv("COURSE_URL")
DOWNLOAD_DIR = 'downloaded_notes'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === SETUP SELENIUM (Chrome) ===
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Remove if you want to see browser
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# === LOGIN ===
driver.get(LOGIN_URL)
driver.find_element(By.NAME, 'username').send_keys(USERNAME)
driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
driver.find_element(By.ID, 'loginbtn').click()
time.sleep(2)

# === GO TO COURSE ===
driver.get(COURSE_URL)
time.sleep(2)

# === FIND LINKS WITH POWERPOINT ICON ===
ppt_links = []
elements = driver.find_elements(By.CSS_SELECTOR, 'li.activity.resource')

for ele in elements:
    try:
        icon = ele.find_element(By.CSS_SELECTOR, 'img.activityicon')
        if 'powerpoint' in icon.get_attribute('src'):
            link = ele.find_element(By.TAG_NAME, 'a').get_attribute('href')
            name = ele.find_element(By.TAG_NAME, 'a').text.strip().replace(' ', '_')
            ppt_links.append((link, name))
    except:
        continue

print(f"Found {len(ppt_links)} PowerPoint files.")

# === DOWNLOAD USING REQUESTS SESSION (PRESERVING COOKIE) ===
session = requests.Session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

for url, name in ppt_links:
    res = session.get(url, allow_redirects=True)
    content_disp = res.headers.get('Content-Disposition', '')
    if 'filename=' in content_disp:
        filename = content_disp.split('filename=')[-1].strip('"')
    else:
        filename = name + '.pptx'
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(res.content)
    print(f"Downloaded: {filename}")

driver.quit()
