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

# Check for admin access - requires both URL parameter and verified email
def is_admin_user():
    """Check if current user has admin privileges."""
    # Check if admin mode is requested via URL
    admin_param = st.query_params.get("admin", "").lower() == "true"
    
    if not admin_param:
        return False
    
    # Check if user email is in admin whitelist
    try:
        # Get admin emails from secrets
        # Support both a single string or a list
        admin_emails_raw = st.secrets.get("ADMIN_EMAILS", [])
        if isinstance(admin_emails_raw, str):
            admin_emails = [email.strip().lower() for email in admin_emails_raw.split(",")]
        else:
            admin_emails = [email.strip().lower() for email in admin_emails_raw]
            
        if not admin_emails:
            if admin_param:
                st.sidebar.error("⚠️ admin_emails not found in secrets")
            return False
        
        # Get current user info from Streamlit Cloud
        user_email = None
        if hasattr(st, "user") and st.user:
            user_email = getattr(st.user, "email", None)
            
        # Normalize current user email
        if user_email:
            user_email = user_email.strip().lower()
            
        # If we have an email, it must be in the whitelist
        if user_email:
            if user_email in admin_emails:
                return True
            else:
                st.sidebar.warning(f"🚫 Email '{user_email}' not in whitelist")
                return False
            
        # If no email is available (user not logged in to Streamlit app)
        is_on_cloud = os.environ.get("STREAMLIT_SERVER_ADDRESS") is not None or \
                      os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud"
        
        if is_on_cloud:
            # On Cloud, if not logged in, we can't verify identity
            st.sidebar.info("ℹ️ Please log in to Streamlit Cloud to verify admin access.")
            return False
            
        # For local development (where st.user.email is always None)
        return True
    except Exception as e:
        # If any error, deny access
        if admin_param:
            st.sidebar.error(f"❌ Auth Error: {str(e)}")
        return False

is_admin = is_admin_user()




# Title and description
st.title("🎬 Local Media Player")
st.markdown("Upload and play your local media files (videos, audio, images) directly in the browser")

# Initialize input handlers
input_handlers = {
    "File Upload": FileUploadInput(),
    "Local Directory": LocalDirectoryInput(),
    "Web Media": WebMediaInput()
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


# Function to render file browser
def render_file_browser():
    """Render the admin file browser UI."""
    st.subheader("📂 Uploaded Files")
    
    cloud_files = st.session_state.get("cloud_files", {})
    
    if not cloud_files:
        st.info("No files uploaded yet.")
        return
    
    st.success(f"📁 {len(cloud_files)} file(s) available")
    
    for filename, file_info in cloud_files.items():
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

