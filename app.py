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
    st.header("📁 Upload Media")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose media files",
        type=[ext[1:] for ext in ALL_SUPPORTED],  # Remove the dot
        accept_multiple_files=True,
        help="Upload video, audio, or image files"
    )
    
    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("**Video:** MP4, WebM, OGG, MOV, AVI")
    st.markdown("**Audio:** MP3, WAV, OGG, M4A, FLAC")
    st.markdown("**Image:** JPG, PNG, GIF, BMP, WebP")

# Main content area
if uploaded_files:
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

else:
    # Welcome message when no files are uploaded
    st.info("👈 Upload media files using the sidebar to get started")
    
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
