# Moodle Notes Downloader & PDF Converter

This Python script automates the download of PowerPoint lecture notes from a Moodle course page and optionally converts them to PDFs.

---

## Features

- Logs into Moodle using Selenium and your credentials  
- Downloads all `.pptx` lecture files from a specified course  
- Converts `.pptx` files to PDF with `--convert` flag (LibreOffice required)  
- Works headlessly 
- Uses Selenium cookies to authenticate download requests  

---

## Setup

1. Clone the repository 

    ```bash
    git clone https://github.com/ThenuThudewattage/moodle-web-scraping.git
    cd moodle-web-scraping
    ```

2. Create and Activate a Virtual Environment
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
    - If you are on **Windows**, activate the virtual environment using:
    ```sh
    .venv\Scripts\activate
    ```

3. Install dependencies

    ```sh
    pip install -r requirements.txt
    ``` 

4. Create a .env file in the project root


5. (Optional) Install LibreOffice for PDF conversion
    ```bash
    brew install --cask libreoffice
    ```

## Usage

1. To download only .pptx files
    ```
    python main.py
    ```

2. To download and convert .pptx files to .pdf
    ```
    python main.py --convert
    ```

## Output
- PowerPoint files are saved in: downloaded_notes/
- PDF files (if converted) are saved in: converted_pdfs/


---
Honestly, I’m questioning my life choices — why did I decide to automate this at midnight? Wouldn’t take much time to do manually anyways :(
