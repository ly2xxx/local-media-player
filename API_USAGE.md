# API Usage Guide

## Starting the API Server

The REST API allows programmatic file uploads, perfect for AI automation and browser tools.

### Start the API (runs on port 5000):
```bash
python api.py
```

### Start Streamlit app (runs on port 8501):
```bash
streamlit run app.py
```

Run both simultaneously for full functionality!

---

## API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Local Media Player API is running"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Upload File
**POST** `/upload`

Upload a media file to the cloud_uploads directory.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (the file to upload)

**Response (Success):**
```json
{
  "success": true,
  "filename": "video.mp4",
  "size": 15728640,
  "size_mb": 15.0,
  "path": "/path/to/cloud_uploads/video.mp4",
  "uploaded_at": "2026-02-03T07:45:00.123456"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Unsupported file type: .exe"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/path/to/video.mp4"
```

**Example (Python):**
```python
import requests

with open('video.mp4', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/upload',
        files={'file': f}
    )
    print(response.json())
```

**Example (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 3. List Files
**GET** `/list`

List all uploaded files.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "files": [
    {
      "filename": "video.mp4",
      "size": 15728640,
      "size_mb": 15.0,
      "uploaded_at": "2026-02-03T07:45:00.123456",
      "type": ".mp4"
    },
    {
      "filename": "audio.mp3",
      "size": 5242880,
      "size_mb": 5.0,
      "uploaded_at": "2026-02-03T07:46:00.123456",
      "type": ".mp3"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/list
```

---

### 4. Delete File
**DELETE** `/delete/<filename>`

Delete a specific file.

**Response (Success):**
```json
{
  "success": true,
  "message": "File deleted: video.mp4"
}
```

**Response (Not Found):**
```json
{
  "success": false,
  "error": "File not found: video.mp4"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/delete/video.mp4
```

---

## AI/Browser Automation Usage

### Using with Clawdbot Browser Tool

The browser tool can now interact with the file uploader or use the API directly:

**Option 1: Use Browser Upload Action**
```python
# Upload via browser automation
browser(
    action="upload",
    targetId="media_file_uploader",  # Widget key
    paths=["C:/Users/vl/Videos/movie.mp4"]
)
```

**Option 2: Use REST API (Recommended)**
```bash
# Direct API upload (faster, no UI needed)
curl -X POST http://localhost:5000/upload \
  -F "file=@C:/Users/vl/Videos/movie.mp4"
```

### Using with Python Scripts

```python
import requests
from pathlib import Path

def upload_media(file_path):
    """Upload a media file via API."""
    url = "http://localhost:5000/upload"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.json().get('success'):
        print(f"✅ Uploaded: {file_path}")
        return response.json()
    else:
        print(f"❌ Failed: {response.json().get('error')}")
        return None

# Upload a file
upload_media("C:/Users/vl/Videos/movie.mp4")
```

---

## Supported File Types

- **Video:** `.mp4`, `.webm`, `.ogg`, `.mov`, `.avi`
- **Audio:** `.mp3`, `.wav`, `.m4a`, `.flac`
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`
- **Documents:** `.pdf`, `.md`, `.txt`

---

## Security Notes

⚠️ **Important:** This API has no authentication. It's designed for local development only.

**For production:**
- Add authentication (API keys, OAuth)
- Add rate limiting
- Validate file sizes
- Implement virus scanning
- Use HTTPS

---

## Troubleshooting

**API won't start:**
- Check if port 5000 is already in use
- Verify Flask is installed: `pip install flask flask-cors`

**Files not appearing in Streamlit:**
- Refresh the Streamlit app (press R in browser)
- Files are stored in `cloud_uploads/` directory
- Check file permissions

**Upload fails:**
- Verify file type is supported
- Check disk space
- Ensure `cloud_uploads/` directory exists and is writable
