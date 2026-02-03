import streamlit as st
from pathlib import Path
from inputs import FileUploadInput, LocalDirectoryInput, WebMediaInput
import json
import os
from datetime import datetime

# ==========================================
# API ENDPOINTS via Query Parameters
# ==========================================
# Handle API requests before rendering any UI
# Usage: ?api=upload, ?api=list, ?api=delete, ?api=health

CLOUD_UPLOADS_DIR = Path(__file__).parent / "cloud_uploads"
CLOUD_UPLOADS_DIR.mkdir(exist_ok=True)

api_action = st.query_params.get("api")

if api_action:
    # API mode - return JSON responses
    
    if api_action == "health":
        # Health check endpoint
        st.json({
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "upload_dir": str(CLOUD_UPLOADS_DIR)
        })
        st.stop()
    
    elif api_action == "list":
        # List all uploaded files
        files = []
        if CLOUD_UPLOADS_DIR.exists():
            for file_path in CLOUD_UPLOADS_DIR.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "name": file_path.name,
                        "size": stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "path": str(file_path)
                    })
        
        st.json({
            "status": "ok",
            "count": len(files),
            "files": files
        })
        st.stop()
    
    elif api_action == "delete":
        # Delete a file
        filename = st.query_params.get("filename")
        if not filename:
            st.json({"status": "error", "message": "filename parameter required"})
            st.stop()
        
        file_path = CLOUD_UPLOADS_DIR / filename
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            st.json({"status": "ok", "message": f"Deleted {filename}"})
        else:
            st.json({"status": "error", "message": "File not found"})
        st.stop()
    
    elif api_action == "upload":
        # Upload endpoint - show instructions
        st.markdown("### 📤 File Upload API")
        st.markdown("""
        To upload files programmatically:
        
        1. **Via Browser Automation:**
           - Navigate to the main page (without `?api=upload`)
           - Use the file uploader widget with key: `media_file_uploader`
           - Files are automatically saved to `cloud_uploads/`
        
        2. **Direct File Access:**
           - Copy files to: `{}`
           - Files will be auto-detected on next page load
        
        **Example (Playwright):**
        ```python
        page.goto("http://localhost:8501")
        page.set_input_files('input[data-testid="stFileUploader"]', 'video.mp4')
        ```
        """.format(CLOUD_UPLOADS_DIR))
        st.stop()
    
    else:
        st.json({"status": "error", "message": f"Unknown API action: {api_action}"})
        st.stop()

# ==========================================
# NORMAL STREAMLIT APP (No API mode)
# ==========================================

# Page configuration
st.set_page_config(
    page_title="Local Media Player",
    page_icon="🎬",
    layout="wide"
)

# Check for admin access using secret token
def is_admin_user():
    """Check if current user has admin privileges.
    
    Uses a secret token approach:
    - Admin visits: ?admin=YOUR_SECRET_TOKEN
    - Token must match ADMIN_TOKEN in secrets.toml
    - Anyone without the secret token cannot access
    """
    # Get the admin param from URL
    admin_param = st.query_params.get("admin", "")
    
    if not admin_param:
        return False
    
    try:
        # Get secret token from secrets
        admin_token = st.secrets.get("ADMIN_TOKEN", "")
        
        if not admin_token:
            return False
        
        # Check if URL token matches secret token
        return admin_param == admin_token
        
    except Exception:
        return False

is_admin = is_admin_user()

# Title and description
st.title("🎬 Local Media Player")
st.markdown("Upload and play your local media files (videos, audio, images) directly in the browser")

# Initialize input handlers
input_handlers = {
    "Local Directory": LocalDirectoryInput(),
    "Web Media": WebMediaInput(),
    "File Upload": FileUploadInput()
}

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Media Source")

    input_method = st.radio(
        "Choose input method",
        list(input_handlers.keys()),
        help="Use 'Local Directory' to stream large files without uploading"
    )

    # Render sidebar for selected input method
    handler = input_handlers[input_method]
    data = handler.render_sidebar()

    # Admin-only: Browse uploaded files button
    if is_admin:
        st.markdown("---")
        st.markdown("### 📂 Admin")
        if st.button("Browse files", use_container_width=True):
            st.session_state.show_file_browser = True

    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("**Video:** MP4, WebM, OGG, MOV, AVI")
    st.markdown("**Audio:** MP3, WAV, OGG, M4A, FLAC")
    st.markdown("**Image:** JPG, PNG, GIF, BMP, WebP")
    st.markdown("**Document:** PDF, MD, TXT")


# Function to render file browser
def render_file_browser():
    """Render the admin file browser UI."""
    st.subheader("📂 Uploaded Files")
    
    cloud_files = st.session_state.get("cloud_files", {})
    
    if not cloud_files:
        st.info("No files uploaded yet.")
        return
    
    st.success(f"📁 {len(cloud_files)} file(s) available")
    
    # Sort files by timestamp in REVERSE order (newest first)
    sorted_files = sorted(
        cloud_files.items(),
        key=lambda x: x[1].get("uploaded_at", ""),
        reverse=True
    )
    
    for filename, file_info in sorted_files:
        with st.expander(f"📄 {filename}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                size_mb = file_info["size"] / (1024 * 1024)
                st.metric("Size", f"{size_mb:.2f} MB")
            with col2:
                st.metric("Type", file_info["type"])
            with col3:
                uploaded_at = file_info.get("uploaded_at", "Unknown")
                if uploaded_at != "Unknown":
                    # Format datetime nicely
                    uploaded_at = uploaded_at.split("T")[0]
                st.metric("Uploaded", uploaded_at)
            
            # Preview based on file type
            file_path = Path(file_info["path"])
            if file_path.exists():
                file_ext = file_path.suffix.lower()
                
                if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                    st.image(str(file_path), use_container_width=True)
                elif file_ext in ['.mp4', '.webm', '.ogg']:
                    st.video(str(file_path))
                elif file_ext in ['.mp3', '.wav', '.m4a', '.flac']:
                    st.audio(str(file_path))
                
                # Download button
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download",
                        data=f.read(),
                        file_name=filename,
                        use_container_width=True
                    )


# Main content area
if st.session_state.get("show_file_browser") and is_admin:
    render_file_browser()
    if st.button("← Back to Media Player"):
        st.session_state.show_file_browser = False
        st.rerun()
elif data:
    handler.render_main_content(data)
else:
    # Welcome message when no files are uploaded/selected
    st.info("👈 Choose a file source in the sidebar to get started")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎥 Video Player")
        st.markdown("Play video files directly in your browser. Supports MP4, WebM, and more.")

    with col2:
        st.markdown("### 🎵 Audio Player")
        st.markdown("Listen to audio files with built-in controls. Supports MP3, WAV, and more.")

    with col3:
        st.markdown("### 🖼️ Image Viewer")
        st.markdown("View images with high quality rendering. Supports JPG, PNG, GIF, and more.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Streamlit • All processing happens in your browser"
    "</div>",
    unsafe_allow_html=True
)
