"""File upload input handler."""
import streamlit as st
from pathlib import Path
from .base import MediaInputHandler


class FileUploadInput(MediaInputHandler):
    """Handler for uploaded media files."""

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

                # Download button
                st.download_button(
                    label="⬇️ Download",
                    data=uploaded_file,
                    file_name=uploaded_file.name,
                    mime=uploaded_file.type
                )
