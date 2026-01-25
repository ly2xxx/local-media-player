"""File upload input handler."""
import streamlit as st
import os
from pathlib import Path
from datetime import datetime
from .base import MediaInputHandler

# Directory for cloud uploads
CLOUD_UPLOADS_DIR = Path(__file__).parent.parent / "cloud_uploads"


class FileUploadInput(MediaInputHandler):
    """Handler for uploaded media files."""

    def __init__(self):
        """Initialize the handler and ensure upload directory exists."""
        super().__init__()
        CLOUD_UPLOADS_DIR.mkdir(exist_ok=True)
        # Initialize session state for tracking uploads
        if "cloud_files" not in st.session_state:
            st.session_state.cloud_files = {}
            # Load existing files from directory
            self._load_existing_files()

    def _load_existing_files(self):
        """Load existing files from cloud_uploads directory."""
        if CLOUD_UPLOADS_DIR.exists():
            for file_path in CLOUD_UPLOADS_DIR.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    st.session_state.cloud_files[file_path.name] = {
                        "path": str(file_path),
                        "size": stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "type": self.get_media_type(file_path.suffix)
                    }

    def _save_to_cloud(self, uploaded_file):
        """Save uploaded file to cloud storage directory."""
        file_path = CLOUD_UPLOADS_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Track in session state
        st.session_state.cloud_files[uploaded_file.name] = {
            "path": str(file_path),
            "size": uploaded_file.size,
            "uploaded_at": datetime.now().isoformat(),
            "type": self.get_media_type(Path(uploaded_file.name).suffix)
        }

    def render_sidebar(self):
        """Render file upload controls in sidebar.

        Returns:
            list: List of uploaded files
        """
        uploaded_files = st.file_uploader(
            "Choose media files",
            type=[ext[1:] for ext in self.ALL_SUPPORTED],  # Remove the dot
            accept_multiple_files=True,
            help="Upload video, audio, or image files"
        )
        
        # Save uploaded files to cloud storage
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.cloud_files:
                    self._save_to_cloud(uploaded_file)
        
        return uploaded_files if uploaded_files else []

    def render_main_content(self, uploaded_files):
        """Render the uploaded files in the main content area.

        Args:
            uploaded_files: List of uploaded files from render_sidebar()
        """
        if not uploaded_files:
            return

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
                    media_type = self.get_media_type(file_extension)
                    st.metric("Type", media_type)

                st.markdown("---")

                # Display media based on type
                if file_extension in self.SUPPORTED_VIDEO:
                    st.video(uploaded_file)

                elif file_extension in self.SUPPORTED_AUDIO:
                    st.audio(uploaded_file)

                elif file_extension in self.SUPPORTED_IMAGE:
                    st.image(uploaded_file, use_container_width=True)

                elif file_extension in self.SUPPORTED_DOCUMENT:
                    if file_extension == '.pdf':
                        # Display PDF using base64 embed
                        import base64
                        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                        uploaded_file.seek(0)  # Reset file pointer for download
                    else:
                        # Display text content for .md and .txt
                        content = uploaded_file.read().decode('utf-8')
                        if file_extension == '.md':
                            st.markdown(content)
                        else:
                            st.text(content)
                        uploaded_file.seek(0)  # Reset file pointer for download

                # Download button
                st.download_button(
                    label="⬇️ Download",
                    data=uploaded_file,
                    file_name=uploaded_file.name,
                    mime=uploaded_file.type
                )
