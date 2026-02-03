"""REST API endpoint for programmatic file uploads.

Run alongside Streamlit app:
    python api.py

API will be available at http://localhost:5000
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Use the same upload directory as the main app
CLOUD_UPLOADS_DIR = Path(__file__).parent / "cloud_uploads"
CLOUD_UPLOADS_DIR.mkdir(exist_ok=True)

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.mp4', '.webm', '.ogg', '.mov', '.avi',  # Video
    '.mp3', '.wav', '.m4a', '.flac',           # Audio
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',  # Images
    '.pdf', '.md', '.txt'                      # Documents
}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Local Media Player API is running'
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to cloud_uploads directory.
    
    Request:
        - file: The file to upload (multipart/form-data)
        
    Response:
        - 200: {success: true, filename: str, size: int, path: str}
        - 400: {success: false, error: str}
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        return jsonify({
            'success': False,
            'error': f'Unsupported file type: {file_ext}'
        }), 400
    
    try:
        # Save file
        file_path = CLOUD_UPLOADS_DIR / file.filename
        file.save(str(file_path))
        
        # Get file info
        stat = file_path.stat()
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'path': str(file_path),
            'uploaded_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/list', methods=['GET'])
def list_files():
    """List all uploaded files.
    
    Response:
        - 200: {files: [{filename, size, uploaded_at, type}, ...]}
    """
    files = []
    
    if CLOUD_UPLOADS_DIR.exists():
        for file_path in CLOUD_UPLOADS_DIR.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'uploaded_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'type': file_path.suffix.lower()
                })
    
    return jsonify({
        'success': True,
        'count': len(files),
        'files': files
    }), 200


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a specific file.
    
    Args:
        filename: Name of the file to delete
        
    Response:
        - 200: {success: true, message: str}
        - 404: {success: false, error: str}
    """
    file_path = CLOUD_UPLOADS_DIR / filename
    
    if not file_path.exists():
        return jsonify({
            'success': False,
            'error': f'File not found: {filename}'
        }), 404
    
    try:
        file_path.unlink()
        return jsonify({
            'success': True,
            'message': f'File deleted: {filename}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Local Media Player API starting...")
    print(f"📁 Upload directory: {CLOUD_UPLOADS_DIR.absolute()}")
    print("📡 API endpoints:")
    print("   - GET  /health       - Health check")
    print("   - POST /upload       - Upload file")
    print("   - GET  /list         - List files")
    print("   - DELETE /delete/<filename> - Delete file")
    print("\n🌐 API available at http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
