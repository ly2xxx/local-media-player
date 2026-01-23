import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Local Media Player",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 Local Media Player")
st.markdown("Upload and play your local media files (videos, audio, images) directly in the browser")

# Supported file types
SUPPORTED_VIDEO = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
SUPPORTED_AUDIO = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
SUPPORTED_IMAGE = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

ALL_SUPPORTED = SUPPORTED_VIDEO + SUPPORTED_AUDIO + SUPPORTED_IMAGE

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Media Source")
    
    input_method = st.radio(
        "Choose input method",
        ["File Upload", "Local Directory"],
        help="Use 'Local Directory' to stream large files without uploading"
    )
    
    selected_file_path = None
    uploaded_files = []

    if input_method == "File Upload":
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose media files",
            type=[ext[1:] for ext in ALL_SUPPORTED],  # Remove the dot
            accept_multiple_files=True,
            help="Upload video, audio, or image files"
        )
    else:
        # Local Discovery
        default_dir = os.getcwd()
        directory_path = st.text_input("Directory Path", value=default_dir)
        
        if os.path.isdir(directory_path):
            # Scan for supported files
            all_files = []
            try:
                for f in os.listdir(directory_path):
                    f_path = Path(directory_path) / f
                    if f_path.is_file() and f_path.suffix.lower() in ALL_SUPPORTED:
                        all_files.append(f)
                
                if all_files:
                    selected_filename = st.selectbox("Select File", all_files)
                    if selected_filename:
                        selected_file_path = Path(directory_path) / selected_filename
                else:
                    st.warning("No supported media files found in this directory")
            except Exception as e:
                st.error(f"Error reading directory: {e}")
        else:
            st.error("Invalid directory path")

    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("**Video:** MP4, WebM, OGG, MOV, AVI")
    st.markdown("**Audio:** MP3, WAV, OGG, M4A, FLAC")
    st.markdown("**Image:** JPG, PNG, GIF, BMP, WebP")

# Main content area
if input_method == "File Upload" and uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) loaded")
    
    # Create tabs for different media types
    tabs = st.tabs([f"📄 {file.name}" for file in uploaded_files])
    
    for tab, uploaded_file in zip(tabs, uploaded_files):
        with tab:
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            # Display file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                size_mb = uploaded_file.size / (1024 * 1024)
                st.metric("Size", f"{size_mb:.2f} MB")
            with col3:
                media_type = "Video" if file_extension in SUPPORTED_VIDEO else \
                            "Audio" if file_extension in SUPPORTED_AUDIO else "Image"
                st.metric("Type", media_type)
            
            st.markdown("---")
            
            # Display media based on type
            if file_extension in SUPPORTED_VIDEO:
                st.video(uploaded_file)
                
            elif file_extension in SUPPORTED_AUDIO:
                st.audio(uploaded_file)
                
            elif file_extension in SUPPORTED_IMAGE:
                st.image(uploaded_file, use_container_width=True)
            
            # Download button
            st.download_button(
                label="⬇️ Download",
                data=uploaded_file,
                file_name=uploaded_file.name,
                mime=uploaded_file.type
            )

elif input_method == "Local Directory" and selected_file_path:
    st.success(f"✅ Loaded: {selected_file_path.name}")
    
    file_extension = selected_file_path.suffix.lower()
    
    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", selected_file_path.name)
    with col2:
        size_mb = selected_file_path.stat().st_size / (1024 * 1024)
        st.metric("Size", f"{size_mb:.2f} MB")
    with col3:
        media_type = "Video" if file_extension in SUPPORTED_VIDEO else \
                    "Audio" if file_extension in SUPPORTED_AUDIO else "Image"
        st.metric("Type", media_type)
    
    st.markdown("---")
    
    # Display media using direct path
    try:
        if file_extension in SUPPORTED_VIDEO:
            st.video(str(selected_file_path))
            
        elif file_extension in SUPPORTED_AUDIO:
            st.audio(str(selected_file_path))
            
        elif file_extension in SUPPORTED_IMAGE:
            st.image(str(selected_file_path), use_container_width=True)
    except Exception as e:
        st.error(f"Error loading media: {e}")

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
