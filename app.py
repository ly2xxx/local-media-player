import streamlit as st
from pathlib import Path
from inputs import FileUploadInput, LocalDirectoryInput, WebMediaInput

# Page configuration
st.set_page_config(
    page_title="Local Media Player",
    page_icon="🎬",
    layout="wide"
)

import os
import json

# Directory for cloud uploads
CLOUD_UPLOADS_DIR = Path(__file__).parent / "cloud_uploads"
CLOUD_UPLOADS_DIR.mkdir(exist_ok=True)

# Handle API requests via query parameters
api_action = st.query_params.get("api")

if api_action == "delete":
    # Admin-only delete file API endpoint
    filename = st.query_params.get("filename")
    admin_token = st.query_params.get("admin", "")
    
    # Verify admin access
    try:
        required_token = st.secrets.get("ADMIN_TOKEN", "")
        if not required_token or admin_token != required_token:
            st.json({"status": "error", "message": "Unauthorized: Invalid or missing admin token"})
            st.stop()
    except Exception:
        st.json({"status": "error", "message": "Unauthorized: Admin token not configured"})
        st.stop()
    
    if not filename:
        st.json({"status": "error", "message": "Missing required parameter: filename"})
        st.stop()
    
    # Delete the file
    file_path = CLOUD_UPLOADS_DIR / filename
    
    if file_path.exists() and file_path.is_file():
        try:
            file_path.unlink()
            st.json({
                "status": "success",
                "message": f"File '{filename}' deleted successfully"
            })
        except Exception as e:
            st.json({
                "status": "error",
                "message": f"Failed to delete file: {str(e)}"
            })
    else:
        st.json({
            "status": "error",
            "message": f"File '{filename}' not found"
        })
    
    st.stop()

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
    
    # Sort files by timestamp in reverse order (newest first)
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
                
                # Download and Delete buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download",
                            data=f.read(),
                            file_name=filename,
                            use_container_width=True
                        )
                with col_btn2:
                    if st.button("🗑️ Delete", key=f"delete_{filename}", use_container_width=True):
                        # Delete the file
                        try:
                            file_path.unlink()
                            # Remove from session state
                            if filename in st.session_state.cloud_files:
                                del st.session_state.cloud_files[filename]
                            st.success(f"Deleted {filename}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete: {str(e)}")


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

