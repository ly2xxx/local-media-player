import streamlit as st
from inputs import FileUploadInput, LocalDirectoryInput, WebMediaInput

# Page configuration
st.set_page_config(
    page_title="Local Media Player",
    page_icon="🎬",
    layout="wide"
)

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

    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("**Video:** MP4, WebM, OGG, MOV, AVI")
    st.markdown("**Audio:** MP3, WAV, OGG, M4A, FLAC")
    st.markdown("**Image:** JPG, PNG, GIF, BMP, WebP")

# Main content area
if data:
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
