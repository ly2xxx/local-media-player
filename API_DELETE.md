# Delete File API

Delete uploaded files programmatically using the query parameter API.

## Endpoint

```
GET /?api=delete&filename=<filename>&admin=<token>
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `api` | Yes | Must be set to `delete` |
| `filename` | Yes | Name of the file to delete (e.g., `video.mp4`) |
| `admin` | Yes | Admin token (must match `ADMIN_TOKEN` in secrets.toml) |

## Authentication

The delete endpoint requires admin authentication. The admin token must be provided in the URL and match the `ADMIN_TOKEN` configured in your Streamlit secrets.

## Response Format

All responses are returned as JSON.

### Success Response

```json
{
  "status": "success",
  "message": "File 'video.mp4' deleted successfully"
}
```

### Error Responses

**Missing filename:**
```json
{
  "status": "error",
  "message": "Missing required parameter: filename"
}
```

**File not found:**
```json
{
  "status": "error",
  "message": "File 'video.mp4' not found"
}
```

**Unauthorized (invalid/missing admin token):**
```json
{
  "status": "error",
  "message": "Unauthorized: Invalid or missing admin token"
}
```

**Delete failed:**
```json
{
  "status": "error",
  "message": "Failed to delete file: <error details>"
}
```

## Examples

### Using curl

```bash
# Delete a file (local development)
curl "http://localhost:8501/?api=delete&filename=video.mp4&admin=YOUR_SECRET_TOKEN"

# Delete a file (Streamlit Cloud)
curl "https://your-app.streamlit.app/?api=delete&filename=video.mp4&admin=YOUR_SECRET_TOKEN"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8501"
ADMIN_TOKEN = "your_secret_token_here"

def delete_file(filename):
    """Delete a file from the server."""
    response = requests.get(
        f"{BASE_URL}/?api=delete&filename={filename}&admin={ADMIN_TOKEN}"
    )
    return response.json()

# Usage
result = delete_file("video.mp4")
print(result)
# Output: {'status': 'success', 'message': "File 'video.mp4' deleted successfully"}
```

### Using Python with error handling

```python
import requests

BASE_URL = "http://localhost:8501"
ADMIN_TOKEN = "your_secret_token_here"

def delete_file(filename):
    """Delete a file with proper error handling."""
    try:
        response = requests.get(
            f"{BASE_URL}/?api=delete",
            params={
                "filename": filename,
                "admin": ADMIN_TOKEN
            }
        )
        
        data = response.json()
        
        if data.get("status") == "success":
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Error: {data['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

# Usage
if delete_file("video.mp4"):
    print("File deleted successfully")
else:
    print("Failed to delete file")
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Admin Token Protection**: Never expose your admin token in public repositories or client-side code
2. **HTTPS Recommended**: Use HTTPS in production to encrypt the admin token in transit
3. **Token Rotation**: Regularly rotate your admin token for security
4. **Audit Logging**: Consider implementing audit logs for delete operations

## UI Alternative

Admins can also delete files through the web UI:

1. Visit the app with admin token: `?admin=YOUR_SECRET_TOKEN`
2. Click "Browse files" in the sidebar
3. Click the "🗑️ Delete" button next to any file

## Configuration

Add your admin token to `.streamlit/secrets.toml`:

```toml
ADMIN_TOKEN = "your_secret_token_here"
```

For Streamlit Cloud, add it in the app settings under "Secrets".
