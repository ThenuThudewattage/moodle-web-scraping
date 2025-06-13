import os
import time
import re
import argparse
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

# === ARGUMENT PARSER ===
parser = argparse.ArgumentParser(description="Download Moodle PPT files and optionally convert to PDF.")
parser.add_argument('--convert', action='store_true', help='Convert downloaded PowerPoint files to PDF')
args = parser.parse_args()

# === ENVIRONMENT VARIABLES ===
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL")
COURSE_URL = os.getenv("COURSE_URL")
DOWNLOAD_DIR = 'downloaded_notes'
PDF_DIR = 'converted_pdfs'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === PDF CONVERSION FUNCTION ===
def convert_to_pdf(input_path, output_dir):
    try:
        subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ], check=True)
        print(f"Converted to PDF: {input_path}")
    except Exception as e:
        print(f"Failed to convert {input_path} to PDF: {e}")

# === SETUP SELENIUM ===
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Remove to see browser
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# === LOGIN TO MOODLE ===
driver.get(LOGIN_URL)
driver.find_element(By.NAME, 'username').send_keys(USERNAME)
driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
driver.find_element(By.ID, 'loginbtn').click()
time.sleep(2)

# === GO TO COURSE PAGE ===
driver.get(COURSE_URL)
time.sleep(2)

# === FIND PPT LINKS ===
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

# === SETUP REQUESTS SESSION FROM SELENIUM COOKIES ===
session = requests.Session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

# === DOWNLOAD FILES AND CONVERT IF REQUESTED ===
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

    if args.convert:
        convert_to_pdf(filepath, PDF_DIR)

driver.quit()
