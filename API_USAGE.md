# API Usage Guide

The Local Media Player supports programmatic file uploads and management through **query parameter-based API endpoints**. This approach works seamlessly on Streamlit Community Cloud since all endpoints share the same port.

## 🔗 Base URL

```
# Local development
http://localhost:8501

# Streamlit Cloud
https://your-app.streamlit.app
```

## 📋 API Endpoints

All API endpoints are accessed via the `?api=<action>` query parameter.

### 1. Health Check

Check if the server is running.

**Request:**
```bash
GET /?api=health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-02-03T12:00:00.000000",
  "upload_dir": "/path/to/cloud_uploads"
}
```

**Example:**
```bash
curl "http://localhost:8501/?api=health"
```

---

### 2. List Files

Get a list of all uploaded files.

**Request:**
```bash
GET /?api=list
```

**Response:**
```json
{
  "status": "ok",
  "count": 2,
  "files": [
    {
      "name": "video.mp4",
      "size": 15728640,
      "uploaded_at": "2026-02-03T12:00:00.000000",
      "path": "/path/to/cloud_uploads/video.mp4"
    },
    {
      "name": "audio.mp3",
      "size": 5242880,
      "uploaded_at": "2026-02-03T11:30:00.000000",
      "path": "/path/to/cloud_uploads/audio.mp3"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8501/?api=list"
```

---

### 3. Delete File

Delete a specific file by name.

**Request:**
```bash
GET /?api=delete&filename=video.mp4
```

**Parameters:**
- `filename` (required): Name of the file to delete

**Response (Success):**
```json
{
  "status": "ok",
  "message": "Deleted video.mp4"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "File not found"
}
```

**Example:**
```bash
curl "http://localhost:8501/?api=delete&filename=video.mp4"
```

---

### 4. Upload File

Upload files programmatically using browser automation.

**Request:**
```bash
GET /?api=upload
```

**Response:**
Returns instructions for uploading files.

**Methods:**

#### Method 1: Browser Automation (Recommended)

Use Playwright, Selenium, or similar tools to interact with the file uploader widget.

**Playwright Example:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to the app
    page.goto("http://localhost:8501")
    
    # Wait for the file uploader to be available
    page.wait_for_selector('input[data-testid="stFileUploader"]')
    
    # Upload file
    page.set_input_files(
        'input[data-testid="stFileUploader"]',
        'path/to/your/video.mp4'
    )
    
    # Wait for upload to complete
    page.wait_for_timeout(2000)
    
    browser.close()
```

**Selenium Example:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://localhost:8501")

# Wait for file uploader
file_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
)

# Upload file
file_input.send_keys("/absolute/path/to/video.mp4")

# Wait for processing
time.sleep(2)

driver.quit()
```

#### Method 2: Direct File Copy

Directly copy files to the upload directory (for local development or server access).

```bash
# Copy file to upload directory
cp video.mp4 cloud_uploads/

# The file will be automatically detected on next page load
```

**Python Example:**
```python
import shutil
from pathlib import Path

source_file = Path("video.mp4")
upload_dir = Path("cloud_uploads")
upload_dir.mkdir(exist_ok=True)

# Copy file to upload directory
shutil.copy(source_file, upload_dir / source_file.name)
```

---

## 🤖 Complete Automation Example

Here's a complete example that uploads a file and verifies it:

```python
from playwright.sync_api import sync_playwright
import requests
import time

BASE_URL = "http://localhost:8501"

def upload_file(file_path):
    """Upload a file using browser automation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to app
        page.goto(BASE_URL)
        
        # Wait for file uploader
        page.wait_for_selector('input[data-testid="stFileUploader"]')
        
        # Upload file
        page.set_input_files(
            'input[data-testid="stFileUploader"]',
            file_path
        )
        
        # Wait for upload
        time.sleep(3)
        
        browser.close()

def list_files():
    """List all uploaded files."""
    response = requests.get(f"{BASE_URL}/?api=list")
    return response.json()

def delete_file(filename):
    """Delete a specific file."""
    response = requests.get(f"{BASE_URL}/?api=delete&filename={filename}")
    return response.json()

# Usage
if __name__ == "__main__":
    # Upload a file
    print("Uploading file...")
    upload_file("video.mp4")
    
    # List files
    print("\nListed files:")
    files = list_files()
    print(files)
    
    # Delete a file
    print("\nDeleting file...")
    result = delete_file("video.mp4")
    print(result)
```

---

## 🔐 Security Notes

1. **API Access:** All API endpoints are publicly accessible. For production, implement authentication.
2. **File Size Limits:** Streamlit has file upload size limits (default 200MB).
3. **Admin Features:** Use `?admin=YOUR_SECRET_TOKEN` for admin file browser access.

---

## 🚀 Streamlit Cloud Deployment

This API approach works perfectly on Streamlit Community Cloud because:
- All endpoints use the same port (Streamlit's port)
- No need for separate Flask/FastAPI servers
- Query parameters work out of the box
- Browser automation can target the deployed URL

**Example with deployed app:**
```python
BASE_URL = "https://your-app.streamlit.app"

# All endpoints work the same way
requests.get(f"{BASE_URL}/?api=health")
requests.get(f"{BASE_URL}/?api=list")
```

---

## 📝 Error Handling

All endpoints return JSON with a `status` field:

**Success:**
```json
{
  "status": "ok",
  ...
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Error description"
}
```

Handle errors appropriately in your automation scripts:

```python
response = requests.get(f"{BASE_URL}/?api=list")
data = response.json()

if data["status"] == "error":
    print(f"Error: {data['message']}")
else:
    print(f"Success! Found {data['count']} files")
```
